

from fastapi import APIRouter
from fastapi.params import Depends
from deps.keycloak import Keycloak
from models.auth import Login
from state.appState import AppState


def getAuthRouter(appState: AppState):
    router = APIRouter()

    @router.post("/login")
    async def login(login: Login, keycloak: Keycloak = Depends(appState.select_keycloak)):
        res = keycloak.login(login.username, login.password, login.totp)
        print("loing", res)
        return res

    return router
