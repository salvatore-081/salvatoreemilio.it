from fastapi import APIRouter, Depends
from fastapi.params import Depends
from starlette.responses import JSONResponse
from state.appState import AppState
from deps.gPRCClient import GPRCClient
from deps.keycloak import Keycloak
from models.user import User
from google.protobuf.json_format import MessageToDict
from grpc import RpcError, StatusCode
from fastapi.security import HTTPBearer
from exceptions import base as base_exceptions, rest as rest_exceptions


def getUsersRouter(appState: AppState):
    router = APIRouter()
    token_auth_scheme = HTTPBearer()

    @router.get("/{email}", response_model=User, responses={400: {"model": rest_exceptions.BadRequest}, 401: {"model": rest_exceptions.Unauthorized}, 403: {"model": rest_exceptions.Forbidden}, 404: {"model": rest_exceptions.NotFound}, 500: {"model": rest_exceptions.InternalServerError}},  response_model_exclude_none=True)
    async def get_user(email: str, gPRCClient: GPRCClient = Depends(appState.select_gPRCClient), keycloak: Keycloak = Depends(appState.select_keycloak), token: str = Depends(token_auth_scheme)):
        try:
            introspection = keycloak.introspect_token(token.credentials)
            keycloak.check_active(introspection)
            keycloak.check_view_users(introspection, email)

            r = await gPRCClient.get_user(email=email)
            return MessageToDict(r)
        except base_exceptions.Forbidden:
            return JSONResponse(
                status_code=403,
                content=rest_exceptions.Forbidden().dict()
            )
        except base_exceptions.Unauthorized:
            return JSONResponse(
                status_code=401,
                content=rest_exceptions.Unauthorized().dict()
            )
        except base_exceptions.BadRequest:
            return JSONResponse(
                status_code=400,
                content=rest_exceptions.BadRequest().dict()
            )
        except RpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                return JSONResponse(
                    status_code=404,
                    content=rest_exceptions.NotFound(detail=e.details()).dict()
                )
            return JSONResponse(
                status_code=500,
                content=rest_exceptions.InternalServerError(
                    detail=e.details(), debug=e.code()).dict()
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content=rest_exceptions.InternalServerError(
                    debug=str(e)).dict()
            )

    # @router.post("", response_model=User, status_code=201, responses={500: {"model": rest_exceptions.InternalServerError}, 409: {"model": rest_exceptions.Conflict}}, response_model_exclude_unset=True, response_model_exclude_none=True)
    # async def add_user(user: User, gPRCClient: GPRCClient = Depends(appState.select_gPRCClient)):
    #     try:
    #         check = await gPRCClient.get_user(email=user.email)
    #         if check['getUser']:
    #             return JSONResponse(
    #                 status_code=409,
    #                 content=rest_exceptions.Conflict(
    #                     detail=f"{user.email} already exists").dict()
    #             )
    #         r = await gPRCClient.add_user(user=user)

    #         return r['addUser']
    #     except Exception as e:
    #         return JSONResponse(
    #             status_code=500,
    #             content=rest_exceptions.InternalServerError(
    #                 debug=str(e)).dict()
    #         )

    return router
