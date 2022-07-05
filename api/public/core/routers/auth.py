from fastapi import APIRouter
from fastapi.params import Depends
from deps.keycloak import Keycloak
from models.auth import LoginInput, LogoutInput, LoginResponse, LogoutResponse
from state.appState import AppState
from exceptions import rest as rest_exceptions
from fastapi.security import HTTPBearer


def getAuthRouter(appState: AppState):
    router = APIRouter()
    token_auth_scheme = HTTPBearer()

    @router.post("/login", status_code=200, response_model=LoginResponse, responses={500: {"model": rest_exceptions.InternalServerError}, 401: {"model": rest_exceptions.Unauthorized}}, response_model_exclude_unset=True, response_model_exclude_none=True)
    async def login(input: LoginInput, keycloak: Keycloak = Depends(appState.select_keycloak)):
        try:
            login = keycloak.login(input.email, input.password, input.totp)
            return login
        except Exception as e:
            raise e

    @router.post("/logout", status_code=200, response_model=LogoutResponse, responses={401: {"model": rest_exceptions.Unauthorized}, 500: {"model": rest_exceptions.InternalServerError}, 400: {"model": rest_exceptions.BadRequest}}, response_model_exclude_unset=True, response_model_exclude_none=True)
    async def logout(input: LogoutInput, keycloak: Keycloak = Depends(appState.select_keycloak), token: str = Depends(token_auth_scheme)):
        try:
            introspection = keycloak.introspect_token(token.credentials)
            keycloak.check_active(introspection)
            keycloak.logout(input.refresh_token)

            return LogoutResponse(refresh_token=input.refresh_token).dict()
        except Exception as e:
            raise e

    return router
