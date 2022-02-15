from fastapi import APIRouter, Depends
from fastapi.params import Depends
from starlette.responses import JSONResponse
from state.appState import AppState
from deps.gPRCClient import GPRCClient
from models.user import User
from models.fastapi_responses import *
from google.protobuf.json_format import MessageToDict
from grpc import RpcError, StatusCode


def getUsersRouter(appState: AppState):
    router = APIRouter()

    @router.get("/{email}", response_model=User, responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},  response_model_exclude_none=True)
    async def get_user(email: str, gPRCClient: GPRCClient = Depends(appState.select_gPRCClient)):
        try:
            r = await gPRCClient.get_user(email=email)
            return MessageToDict(r)
        except RpcError as e:
            match e.code():
                case StatusCode.NOT_FOUND:
                    return JSONResponse(
                        status_code=404,
                        content=NotFound(detail=e.details()).dict()
                    )
                case _:
                    return JSONResponse(
                        status_code=500,
                        content=InternalServerError(details=e.details(), debug=e.code()).dict()
                    )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content=InternalServerError(debug=str(e)).dict()
            )

    @router.post("", response_model=User, status_code=201, responses={500: {"model": InternalServerError}, 409: {"model": Conflict}}, response_model_exclude_unset=True, response_model_exclude_none=True)
    async def add_user(user: User, gPRCClient: GPRCClient = Depends(appState.select_gPRCClient)):
        try:
            check = await gPRCClient.get_user(email=user.email)
            if check['getUser']:
                return JSONResponse(
                    status_code=409,
                    content=Conflict(
                        detail=f"{user.email} already exists").dict()
                )
            r = await gPRCClient.add_user(user=user)

            return r['addUser']
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content=InternalServerError(debug=str(e)).dict()
            )

    return router
