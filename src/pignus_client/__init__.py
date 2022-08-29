"""Pignus Client

"""
import requests
import os


class PignusClient:

    def __init__(self, api_url: str = None, api_client_id: str = None, api_key: str = None):
        """
        :unit-test: TestRest.test____init__()
        """
        if api_url:
            self.api_url = api_url
        else:
            self.api_url = os.environ.get("PIGNUS_API_URL")

        if api_client_id:
            self.api_client_id = api_client_id
        else:
            self.api_client_id = os.environ.get("PIGNUS_API_CLIENT_ID")

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.environ.get("PIGNUS_API_KEY")

        self.die_response_level = None
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            # "User-Agent": settings.client["API_UA"],
        }

    def __repr__(self):
        """
        :unit-test: TestRest::test____repr__
        """
        return "<PignusClient>"

    def images_get(self, payload: dict = {}) -> dict:
        """Get Images on the Pignus Api, against /images
        :unit-test: TestClient:test__images_get
        """
        response = self.request("images", payload)
        return response

    def request(
        self, url: str, payload: dict = {}, method: str = "GET"
    ) -> requests.Response:
        """Make a request on the Pignus Api.
        :unit-test: TestClient:test__request
        """
        request_args = {
            "headers": self.headers,
            "method": method,
            "url": "%s/%s" % (self.api_url, url),
        }
        if payload:
            if request_args["method"] in ["GET", "DELETE"]:
                request_args["params"] = payload
            elif request_args["method"] == "POST":
                for key, value in payload.items():
                    if isinstance(value, bool):
                        payload[key] = str(value).lower()
                request_args["json"] = payload

        response = requests.request(**request_args)
        if response.status_code >= 500:
            log.error("Pignus Api Error")

        if self.die_response_level:
            if response.status_code >= self.die_response_level:
                print("-- Request Failed --")
                print("Url\t%s" % request_args["url"])
                print("Status\t%s" % response.status_code)
                print("Method\t%s" % request_args["method"])
                # if payload:
                #     print("Params\t%s" % payload)
                print("Response")
                print(response.text)

        return response

# End File: pignus/src/pignus_client/__init__.py