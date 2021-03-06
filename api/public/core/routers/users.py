from fastapi import APIRouter, Depends
from fastapi.params import Depends
from starlette.responses import JSONResponse
from state.appState import AppState
from deps.gRPCClient import GRPCClient
from deps.keycloak import Keycloak
from models.user import UpdateUserInputPayload, User, UserList
from google.protobuf.json_format import MessageToDict
from fastapi.security import HTTPBearer
from exceptions import rest as rest_exceptions


def getUsersRouter(appState: AppState):
    router = APIRouter()
    token_auth_scheme = HTTPBearer()

    @router.get("", response_model=UserList, responses={400: {"model": rest_exceptions.BadRequest}, 404: {"model": rest_exceptions.NotFound}, 500: {"model": rest_exceptions.InternalServerError}},  response_model_exclude_none=True)
    async def get_user_list(gRPCClient: GRPCClient = Depends(appState.select_gPRCClient)):
        try:
            r = await gRPCClient.get_user_list()
            return MessageToDict(r)
        except Exception as e:
            raise e

    @router.get("/{email}", response_model=User, responses={400: {"model": rest_exceptions.BadRequest}, 404: {"model": rest_exceptions.NotFound}, 500: {"model": rest_exceptions.InternalServerError}},  response_model_exclude_none=True)
    async def get_user(email: str, gRPCClient: GRPCClient = Depends(appState.select_gPRCClient)):
        try:
            r = await gRPCClient.get_user(email=email)
            return MessageToDict(r)
        except Exception as e:
            raise e

    @router.put("/{email}", response_model=User, responses={400: {"model": rest_exceptions.BadRequest}, 401: {"model": rest_exceptions.Unauthorized}, 403: {"model": rest_exceptions.Forbidden}, 404: {"model": rest_exceptions.NotFound}, 500: {"model": rest_exceptions.InternalServerError}},  response_model_exclude_none=True)
    async def put_user(email: str, payload: UpdateUserInputPayload, gRPCClient: GRPCClient = Depends(appState.select_gPRCClient), keycloak: Keycloak = Depends(appState.select_keycloak), token: str = Depends(token_auth_scheme)):
        try:
            introspection = keycloak.introspect_token(token.credentials)
            keycloak.check_active(introspection)
            keycloak.check_manage_users(introspection, email)

            r = await gRPCClient.update_user(email, payload)
            return MessageToDict(r)
        except Exception as e:
            raise e

    return router
