from fastapi import FastAPI, APIRouter
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from grpc import RpcError, StatusCode
from state.appState import AppState
from .routers import users, auth
from .graphql.query import getQuery
from .graphql.mutation import getMutation
from .graphql.subscription import getSubscription
from .graphql.schema import SCHEMA
from os import system
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
from exceptions import rest as rest_exceptions, base as base_exceptions
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError

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

    @app.exception_handler(RpcError)
    async def rpcError_exception_handler(request: Request, e: RpcError):
        if e.code() == StatusCode.INVALID_ARGUMENT:
            return JSONResponse(
                status_code=400,
                content=rest_exceptions.BadRequest().dict()
            )
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

    @app.exception_handler(base_exceptions.BadRequest)
    async def bad_request_exception_handler(request: Request, e: base_exceptions.BadRequest):
        return JSONResponse(
            status_code=400,
            content=rest_exceptions.BadRequest().dict()
        )

    @app.exception_handler(KeycloakGetError)
    async def keycloak_get_error_exception_handler(request: Request, e: KeycloakGetError):
        return JSONResponse(
            status_code=400,
            content=rest_exceptions.BadRequest(
                detail="Invalid refresh token").dict()
        )

    @app.exception_handler(base_exceptions.Unauthorized)
    async def unauthorized_exception_handler(request: Request, e: base_exceptions.Unauthorized):
        return JSONResponse(
            status_code=401,
            content=rest_exceptions.Unauthorized().dict()
        )

    @app.exception_handler(KeycloakAuthenticationError)
    async def keycloak_authentication_error_exception_handler(request: Request, e: KeycloakAuthenticationError):
        return JSONResponse(
            status_code=401,
            content=rest_exceptions.Unauthorized().dict()
        )

    @app.exception_handler(base_exceptions.Forbidden)
    async def forbidden_exception_handler(request: Request, e: base_exceptions.Forbidden):
        return JSONResponse(
            status_code=403,
            content=rest_exceptions.Forbidden().dict()
        )

    graphqlApp = GraphQL(make_executable_schema(
        SCHEMA, getQuery(appState), getMutation(appState), getSubscription(appState)), keepalive=None)

    app.mount("/graphql", graphqlApp)
except Exception as e:
    from logging import getLogger
    getLogger("uvicorn.error").log(
        level=50, msg=f"Startup failed: {e}")
    system("pkill python3")
