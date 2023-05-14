import asyncio

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2AuthorizationCodeBearer
from fief_client import FiefAccessTokenInfo, FiefAsync
from fief_client.integrations.fastapi import FiefAuth


fief = FiefAsync(
    "https://xxxxx.fief.dev",
    "xxxxx",
    "xxxxx",
)

scheme = OAuth2AuthorizationCodeBearer(
    "https://xxxxx.fief.dev/authorize",
    "https://xxxxxxx.fief.dev/api/token",
    scopes={"openid": "openid", "offline_access": "offline_access"},
    auto_error=False,
)
