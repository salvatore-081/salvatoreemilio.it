from fastapi import APIRouter, Depends
from fastapi.params import Depends
from starlette.responses import JSONResponse
from state.appState import AppState
from deps.gql import GQLClient
from models.user import User
from models.fastapi_responses import *


def getUsersRouter(appState: AppState):
    router = APIRouter()

    @router.get("/{email}", response_model=User, responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},  response_model_exclude_none=True)
    async def get_user(email: str, gqlClient: GQLClient = Depends(appState.select_gqlClient)):
        try:
            r = await gqlClient.get_user(email=email)
            if not r['getUser']:
                return JSONResponse(
                    status_code=404,
                    content=NotFound(detail=f"{email} not found").dict()
                )
            else:
                return r['getUser']
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content=InternalServerError(debug=str(e)).dict()
            )

    @router.post("", response_model=User, status_code=201, responses={500: {"model": InternalServerError}, 409: {"model": Conflict}}, response_model_exclude_unset=True, response_model_exclude_none=True)
    async def add_user(user: User, gqlClient: GQLClient = Depends(appState.select_gqlClient)):
        try:
            check = await gqlClient.get_user(email=user.email)
            if check['getUser']:
                return JSONResponse(
                    status_code=409,
                    content=Conflict(
                        detail=f"{user.email} already exists").dict()
                )
            r = await gqlClient.add_user(user=user)

            return r['addUser']
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content=InternalServerError(debug=str(e)).dict()
            )

    return router
