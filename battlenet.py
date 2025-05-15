from typing import Any
import requests
from enum import Enum


    
class BattleNetAPI:
    class REGION(Enum):
        US = "us"
        EU = "eu"
        APAC = "apac"
        CN = "cn"

    class AUTH_REGION(Enum):
        US_EU_APAC = 1
        CN = 2

    AUTH_URLS = {
        AUTH_REGION.US_EU_APAC: "https://oauth.battle.net//token",
        AUTH_REGION.CN: "https://oauth.battlenet.com.cn/token"
    }

    API_DOMAIN_NAME = "api.blizzard.com"

    REALMS_INDEX_ROUTE = "/data/wow/connected-realm/index"

    def __init__(self, token: str, region: REGION, custom_url: str = "", port: int = 443):
        self.region = region
        if custom_url == "":
            self.api_url = f"https://{self.region.value}.{self.API_DOMAIN_NAME}"
        else:
            self.api_url = custom_url
        self.port = port

    def set_auth_domain_name(self, auth_domain_name: str):
        self.auth_domain_name = auth_domain_name

    def set_api_domain_name(self, api_domain_name: str):
        self.api_url = api_domain_name

    def set_port(self, port: int):
        self.port = port        

    def get(self, endpoint: str, params: dict[str, str] = {}) -> Any:
        response = requests.get(f"{self.api_url}:{self.port}{endpoint}",
                                headers={"Authorization": "Bearer {self.token}"}, params=params)
        response.raise_for_status()
        return response.json()

    def get_connected_realms(self) -> None:
        params = {"namespace": f"dynamic-{self.region}", "locale": "en_US"}
        response = self.get(self.REALMS_INDEX_ROUTE, params)
        print(response)

def auth_custom(client_id: str, client_secret: str, url: str, port: int) -> str:
    response = requests.post(f"{url}:{port}/oauth/token", data={"grant_type": "client_credentials"}, auth=(client_id, client_secret))
    response.raise_for_status()
    return response.json()["access_token"]

def auth(client_id: str, client_secret: str, auth_region: BattleNetAPI.AUTH_REGION) -> str:
    return auth_custom(client_id, client_secret, BattleNetAPI.AUTH_URLS[auth_region], 443)
