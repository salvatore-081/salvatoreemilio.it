from fastapi import FastAPI, APIRouter
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from state.appState import AppState
from .routers import users, auth
from .graphql.query import getQuery
from .graphql.mutation import getMutation
from .graphql.schema import SCHEMA
from os import system
import logging

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

    gqlApp = GraphQL(make_executable_schema(
        SCHEMA, getQuery(appState), getMutation(appState)), keepalive=30)

    app.mount("/graphql", gqlApp)
except Exception as e:
    import logging
    logging.getLogger("uvicorn.error").log(
        level=50, msg=f"Startup failed: {e}")
    system("pkill python3")

    # # Set all CORS enabled origins
    # app.add_middleware(
    #         CORSMiddleware,
    #         allow_origins=["*"],
    #         allow_credentials=True,
    #         allow_methods=["*"],
    #         allow_headers=["*"],
    #     )
