from logging import exception
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.params import Depends
from pydantic.main import BaseModel
from starlette.responses import JSONResponse
from state.appState import AppState
from deps.gql import GQLClient
from models.user import User


class InternalServerError(BaseModel):
    message: str
    debug: Optional[str]


class NotFound(BaseModel):
    message: str


class Conflict(BaseModel):
    message: str


def getUsersRouter(appState: AppState):
    router = APIRouter()

    @router.get("/{email}", response_model=User, responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},  response_model_exclude_none=True)
    async def get_user(email: str, gqlClient: GQLClient = Depends(appState.select_gqlClient)):
        try:
            r = await gqlClient.get_user(email=email)
            if not r['getUser']:
                return JSONResponse(
                    status_code=404,
                    content={"message": f"{email} not found"}
                )
            else:
                return r['getUser']
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"message": "unexpected error", "debug": str(e)}
            )

    @router.post("", response_model=User, status_code=201, responses={500: {"model": InternalServerError}, 409: {"model": Conflict}}, response_model_exclude_unset=True, response_model_exclude_none=True)
    async def add_user(user: User, gqlClient: GQLClient = Depends(appState.select_gqlClient)):
        try:
            check = await gqlClient.get_user(email=user.email)
            if check['getUser']:
                return JSONResponse(
                    status_code=409,
                    content={"message": f"{user.email} already exists"}
                )
            r = await gqlClient.add_user(user=user)

            return r['addUser']
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"message": "unexpected error", "debug": str(e)}
            )

    return router
