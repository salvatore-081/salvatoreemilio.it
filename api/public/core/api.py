from typing import Any
from fastapi import FastAPI, APIRouter
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL, WebSocketConnectionError
from state.appState import AppState
from .routers import users, auth
from .graphql.query import getQuery
from .graphql.mutation import getMutation
from .graphql.subscription import getSubscription
from .graphql.schema import SCHEMA
from os import system

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

    app.include_router(api_router, prefix="")

    def on_connect(websocket, params: Any):
        auth = params.get("Authorization")
        if not auth or not auth.startswith("Bearer ") or len(auth) < 7:
            raise WebSocketConnectionError("invalid Authorization")
        websocket.scope["connection_params"] = {
            "access_token": auth[7:],
        }

    def context_value(request):
        context = {'request': request}
        if request.scope["type"] == "websocket":
            context.update(request.scope["connection_params"])

        return context

    graphqlApp = GraphQL(make_executable_schema(
        SCHEMA, getQuery(appState), getMutation(appState), getSubscription(appState)), keepalive=None, context_value=context_value, on_connect=on_connect)

    app.mount("/graphql", graphqlApp)
except Exception as e:
    from logging import getLogger
    getLogger("uvicorn.error").log(
        level=50, msg=f"Startup failed: {e}")
    system("pkill python3")
