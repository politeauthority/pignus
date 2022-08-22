"""Auth Utility

"""
import base64
from datetime import timedelta
import os
import random
import re
import rsa
import secrets

from pignus_api.collections.api_keys import ApiKeys
from pignus_api.models.api_key import ApiKey
from pignus_api.models.user import User
from pignus_api.utils import log
from pignus_api.utils import misc_server
from pignus_api.utils import date_utils
from pignus_api import settings


class Auth:

    def __init__(self):
        """Set up the Auth class grabbing the location of the RSA Key pair on disk.
        :unit-test: TestAuth::test____init__
        """
        self.path_keys = misc_server.get_pignus_key_path()
        self.path_public_key = os.path.join(self.path_keys, "id_rsa.pub")
        self.path_private_key = os.path.join(self.path_keys, "id_rsa")
        self.public_key = settings.server["KEYS"]["PUBLIC"]
        self.private_key = settings.server["KEYS"]["PRIVATE"]

    def auth_api_key(self, request_api_key: str) -> ApiKey:
        """Take a plaintext ApiKey and check if it's a valid key. If so, return the ApiKey object, if
        not return False. @todo: Check the key's expiration date and make sure it's in the future.
        """
        api_keys = ApiKeys().get_all_enabled()
        matched_key = False
        for api_key in api_keys:
            decrypted = self.decrypt(api_key.key)
            if decrypted == request_api_key:
                matched_key = True
                break

        if not matched_key:
            return False

        if not api_key.expiration:
            return api_key
        else:
            return api_key

    def generate_keys(self, overwrite=False) -> tuple:
        """Generate a public/private key pair to use for encrypting Pignus api keys.
        """
        if not os.path.exists(self.path_keys):
            os.makedirs(self.path_keys)

        if os.path.exists(self.path_public_key):
            current_public = self.path_public_key
        else:
            current_public = None

        if current_public and not overwrite:
            log.debug(
                "Found existing Pignus key pair, and overwrite set False, NOT creating new keys")
            return False

        elif current_public and overwrite:
            log.warning("Overwriting existing Pignus key pair")

        self.public_key, self.private_key = rsa.newkeys(512)

        # Save the public key
        with open(self.path_public_key, "w") as out:
            pickle_public_key = misc_server.pickle_in(self.public_key)
            out.write(pickle_public_key)

        # Save the private key
        with open(self.path_private_key, "w") as out:
            pickle_private_key = misc_server.pickle_in(self.private_key)
            out.write(pickle_private_key)

        return (self.public_key, self.private_key)

    def rotate_key_pair(self) -> bool:
        """Roatate the Pignus RSA key pair, reencrypting all the existing ApiKey's with the new key
        pair.
        # @todo: Set all other keys to disabled and set a note.
        """
        current_private_key = self.private_key

        public_key, private_key = self.generate_keys(overwrite=True)

        # Get all ApiKeys are encrypt them
        api_keys = ApiKeys().get_all()

        if len(api_keys) == 0:
            log.warning("Found 0 ApiKeys to reencrypt")
            pass
        elif not isinstance(current_private_key, rsa.key.PrivateKey):
            log.error(
                "Current private key is unuseable, all current ApiKeys need to be regenerated.")
        else:
            self.reencrypt_keys(api_keys, current_private_key, private_key)

        self.store_keys(public_key, private_key)

        return False

    def reencrypt_keys(
        self,
        current_api_keys: list,
        old_private_key: rsa.key.PrivateKey,
        new_private_key: rsa.key.PrivateKey
    ) -> bool:
        """Rencrypt all ApiKey's currenty encrypted with the old key.
        @params
            current_api_keys: list
                All current ApiKeys that we need to reencrypt.
            old_private_key: rsa.key.PrivateKey
                The private key that was previously encryting all ApiKeys
            new_private_key: rsa.key.PrivateKey
        """
        if not current_api_keys:
            return True
        for api_key in current_api_keys:
            decrypted_key = self.decrypt_with_key(old_private_key, api_key.key)
            if not decrypted_key:
                log.error(
                    "Unable to rencrypt keys. %s keys will need to be regenerated." % (
                        len(current_api_keys)))
                ApiKeys().disable_all()
                return False
            encrypted_key = self.encrypt_with_key(new_private_key, decrypted_key)
            api_key.key = encrypted_key
            api_key.save()
        log.info("Reencrypted %s ApiKeys" % len(current_api_keys))
        return True

    def encrypt(self, data: str) -> str:
        """Encrypt a given string with the Pignus public key stored in AWS SSM, returning a base64
        encoded value, making the value more portable and more easily stored.
        """
        ecrypted_data = self.encrypt_with_key(self.public_key, data)
        return ecrypted_data

    def encrypt_with_key(self, public_key: rsa.key.PrivateKey, data: str) -> str:
        """Encrypt a given string with a given public key, returning a base64 encoded value, making the
        value more portable and more easily stored.
        """
        ecrypted_data = rsa.encrypt(data.encode(), public_key)
        encoded_encrypted_data = base64.b64encode(ecrypted_data)
        encoded_encrypted_data = encoded_encrypted_data.decode()
        return encoded_encrypted_data

    def decrypt(self, data: str) -> str:
        """Decrypt a given string, which is a base64ed encrypted string."""
        decoded_data = base64.b64decode(data)
        try:
            decrypted_data = rsa.decrypt(decoded_data, self.private_key)
        except rsa.pkcs1.DecryptionError:
            log.error("Unable to decrypt data with key %s" % self.path_private_key)
            return False
        if decrypted_data:
            return decrypted_data.decode()
        return False

    def decrypt_with_key(self, key: rsa.key.PrivateKey, data: str) -> str:
        """Decrypt a given string, which is a base64ed encrypted string."""
        decoded_data = base64.b64decode(data)
        try:
            decrypted_data = rsa.decrypt(decoded_data, key).decode()
            return decrypted_data
        except rsa.pkcs1.DecryptionError as e:
            log.error("Could not decrypt data: %s" % e, exception=e)
            return False

    def generate_api_key(self) -> str:
        """Generate a random api key."""
        avail_chars = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
            "s", "t", "u", "v", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
        ]
        the_secret = secrets.token_urlsafe(30)
        skip_strs = ["-", "_"]
        for skip_str in skip_strs:
            if skip_str not in the_secret:
                continue

            skips = [m.start() for m in re.finditer(skip_str, the_secret)]

            for skip in skips:
                temp = list(the_secret)
                temp[skip] = avail_chars[random.randint(0, len(avail_chars) - 1)]
                the_secret = "".join(temp)

        return the_secret

    def create_user(self) -> dict:
        """Create the first User and ApiKey pair for Pignus_api. """
        user = User()
        if not user.get_by_name("pignus-admin"):
            user.name = "pignus-admin"
            user.role_id = 1
            user.save()

        plain_text_key = self.generate_api_key()
        api_key = ApiKey()
        api_key.key = self.encrypt(plain_text_key)
        api_key.user_id = user.id
        api_key.expiration = date_utils.now() + timedelta(hours=8)
        api_key.save()
        return {
            "user": user,
            "api_key": plain_text_key
        }

    # def store_keys(self):


# End File: pignus/src/pignus_api/utils/auth.py
