from typing import Any
from fastapi import FastAPI, APIRouter
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from state.appState import AppState
from .routers import users, auth
from .graphql.query import getQuery
from .graphql.mutation import getMutation
from .graphql.subscription import getSubscription
from .graphql.schema import SCHEMA
from os import system
from fastapi.middleware.cors import CORSMiddleware

try:
    appState = AppState()

    api_router = APIRouter()

    users_router = users.getUsersRouter(appState)
    auth_router = auth.getAuthRouter(appState)

    api_router.include_router(users_router, prefix="/users", tags=["users"])
    api_router.include_router(auth_router, prefix=("/auth"), tags=["auth"])

    app = FastAPI(
        title="salvatoreemilio.it", openapi_url="/openapi.json"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="")

    graphqlApp = GraphQL(make_executable_schema(
        SCHEMA, getQuery(appState), getMutation(appState), getSubscription(appState)), keepalive=None)

    app.mount("/graphql", graphqlApp)
except Exception as e:
    from logging import getLogger
    getLogger("uvicorn.error").log(
        level=50, msg=f"Startup failed: {e}")
    system("pkill python3")
