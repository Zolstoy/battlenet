import requests
from enum import Enum

class BattleNetAPI:
    class REGION(Enum):
        US = "us"
        EU = "eu"
        APAC = "apac"
        CN = "cn"

    AUTH_DOMAIN_NAME = "oauth.battle.net"
    API_DOMAIN_NAME = "api.blizzard.com"

    def __init__(self, client_id: str, client_secret: str, region: REGION): 
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        self.token = self.get_access_token()

    def get_access_token(self):
        url = f"{self.AUTH_DOMAIN_NAME}/token"
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, data=data, auth=(self.client_id, self.client_secret))
        response.raise_for_status()
        return response.json()["access_token"]

    def get(self, endpoint: str, params: dict[str, str] = {}):
        params["access_token"] = self.token
        url = f"https://{self.region}{self.API_DOMAIN_NAME}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # Example: Get WoW profile
    def get_wow_profile(self, realm, character_name):
        endpoint = f"/profile/wow/character/{realm}/{character_name.lower()}"
        params = {"namespace": f"profile-{self.region}", "locale": "en_US"}
        return self.get(endpoint, params)

# Example usage:
# api = BattleNetAPI("your_client_id", "your_client_secret")
# profile = api.get_wow_profile("realm-name", "character-name")
# print(profile)