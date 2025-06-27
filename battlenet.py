from typing import Any
import requests
from enum import Enum

class REGION(Enum):
    US = "us"
    EU = "eu"
    APAC = "apac"
    CN = "cn"

AUTH_DOMAINS = {
    REGION.US: "oauth.battle.net",
    REGION.EU: "oauth.battle.net",
    REGION.APAC: "oauth.battle.net",
    REGION.CN: "oauth.battlenet.com.cn"
}

API_DOMAIN = "api.blizzard.com"

REALMS_INDEX_ROUTE = "/data/wow/connected-realm/index"

class Session:
    def __init__(self, token: str, region: REGION, api_domain: str = "", port: int = 443):
        self.token = token
        self.region = region
        if api_domain == "":
            self.full_api_domain = f"{self.region.value}.{API_DOMAIN}"
        else:
            self.full_api_domain = api_domain
        self.port = port

    def set_api_domain(self, api_domain_name: str):
        self.full_api_domain = api_domain_name

    def set_port(self, port: int):
        self.port = port        

    def get(self, endpoint: str, params: dict[str, str] = {}) -> Any:
        response = requests.get(f"{self.full_api_domain}:{self.port}{endpoint}",
                                headers={"Authorization": "Bearer {self.token}"}, params=params)
        response.raise_for_status()
        return response.json()

    def get_connected_realms(self) -> None:
        params = {"namespace": f"dynamic-{self.region}", "locale": "en_US"}
        response = self.get(REALMS_INDEX_ROUTE, params)
        print(response)

def auth(client_id: str, client_secret: str, region: REGION,
         auth_domain: str | None = None, api_domain: str | None = None,
         port: int = 443, https: bool = True) -> Session:
    if auth_domain is None:
        auth_domain = AUTH_DOMAINS[region]
    if api_domain is None:
        api_domain = f"{region.value}.{API_DOMAIN}"
    if https:
        url = "https://"
    else:
        url = "http://"

    auth_url = f"{url}{auth_domain}:{port}/token"
    
    response = requests.post(auth_url, data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    })

    response.raise_for_status()

    token = response.json().get("access_token")

    if token is None:
        raise ValueError("Failed to obtain access token from BattleNet API")
    return Session(token, region, api_domain, port)

    