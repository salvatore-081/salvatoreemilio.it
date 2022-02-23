

from logging import debug
from fastapi import APIRouter
from fastapi.params import Depends
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError
from starlette.responses import JSONResponse
from deps.keycloak import Keycloak
from models.auth import LoginInput, LogoutInput, LoginResponse, LogoutResponse
from state.appState import AppState
from models.rest_responses import *


def getAuthRouter(appState: AppState):
    router = APIRouter()

    @router.post("/login", status_code=200, response_model=LoginResponse, responses={500: {"model": InternalServerError}, 401: {"model": Unauthorized}}, response_model_exclude_unset=True, response_model_exclude_none=True)
    async def login(input: LoginInput, keycloak: Keycloak = Depends(appState.select_keycloak)):
        try:
            login = keycloak.login(input.email, input.password, input.totp)
            return login
        except Exception as e:
            if isinstance(e, KeycloakAuthenticationError):
                return JSONResponse(
                    status_code=401,
                    content=Unauthorized().dict()
                )
            return JSONResponse(
                status_code=500,
                content=InternalServerError(debug=str(e)).dict()
            )

    @router.post("/logout", status_code=200, response_model=LogoutResponse, responses={500: {"model": InternalServerError}, 400: {"model": BadRequest}}, response_model_exclude_unset=True, response_model_exclude_none=True)
    async def logout(input: LogoutInput, keycloak: Keycloak = Depends(appState.select_keycloak)):
        try:
            keycloak.logout(input.refresh_token)
            return LogoutResponse().dict()
        except Exception as e:
            if isinstance(e, KeycloakGetError):
                return JSONResponse(
                    status_code=400,
                    content=BadRequest(detail="Invalid refresh token").dict()
                )
            return JSONResponse(
                status_code=500,
                content=InternalServerError(debug=str(e)).dict()
            )

    return router
