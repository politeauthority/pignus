"""Pignus Sentry

"""
from pignus_client import PignusClient
from pignus_api.utils import log


class PignusSentry:

    def __init__(self):
        self.pigus_api = PignusClient()

    def run(self):
        print("Running Pignus Sentry")

        self.sentry_sync()

    def sentry_sync(self):
        print("Sentry Sync")
        request = self.pigus_api.images_get()
        requset_data = request.json()
        log.info("Images")
        for image in requset_data["objects"]:
            log.info("%s\t-%s" % (image["id"], image["name"]))

if __name__ == "__main__":
    PignusSentry().run()


# End File: pignus/src/pignus_sentry/pignus_sentry.py
