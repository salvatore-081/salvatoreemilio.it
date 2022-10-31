from fastapi import FastAPI, APIRouter
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from grpc import RpcError
from deps.config import Config
from state.appState import AppState
from .routers import users, auth, misc, projects
from .graphql.query import newQuery
from .graphql.mutation import newMutation
from .graphql.subscription import newSubscription
from .graphql.schema import SCHEMA
from .graphql.scalars import newBase64Scalar
from os import system
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
from exceptions import rest as rest_exceptions, base as base_exceptions
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError
import logging
from loguru import logger
from graphql import GraphQLError
from gunicorn.glogging import Logger
from sys import stdout
from ariadne.asgi.handlers import GraphQLTransportWSHandler

CONFIG_PATH: str = "config.json"

class Application():
    def __init__(self):
        try:
            self.config: Config = Config(CONFIG_PATH) 
            self.appState = AppState(self.config)
            self.app = self.__newApp()
            self.options = self.__newOptions()
        except Exception as e:
            logging.getLogger("uvicorn.error").log(
                level=50, msg=f"Startup failed: {e}")
            system("pkill python3")
    
    def __newApiRouter(self) -> APIRouter:
        try:
            api_router = APIRouter()

            api_router.include_router(auth.getAuthRouter(self.appState), prefix=("/auth"), tags=["auth"])
            api_router.include_router(users.getUsersRouter(self.appState), prefix="/users", tags=["users"])
            api_router.include_router(projects.newProjectsRouter(self.appState), prefix=("/projects"), tags=["projects"])
            api_router.include_router(misc.getMiscRouter(), prefix=("/misc"), tags=["misc"])

            return api_router
        except Exception as e:
            raise e
    
    def __newApp(self)-> FastAPI:
        try:
            app = FastAPI(title="salvatoreemilio.it", openapi_url="/openapi.json")
            app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
            app.include_router(self.__newApiRouter(), prefix="")
            app.add_exception_handler(RpcError, self.appState.gRPCClient.rpcError_exception_handler)
                
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
            
            @app.exception_handler(Exception)
            async def fallback_exception_handler(request: Request, e: base_exceptions.Forbidden):
                return JSONResponse(
                    status_code=500,
                    content=rest_exceptions.InternalServerError(
                    debug=str(e)).dict()
                )

            graphqlApp = GraphQL(make_executable_schema(
                SCHEMA, newQuery(self.appState), newMutation(self.appState), newSubscription(self.appState), newBase64Scalar()), websocket_handler=GraphQLTransportWSHandler())

            app.mount("/graphql", graphqlApp)
            return app
        except Exception as e:
            raise e

    def __newOptions(self):
        logging.root.setLevel(self.config.logLevel)

        seen = set()
        for name in [
            *logging.root.manager.loggerDict.keys(),
            "gunicorn",
            "gunicorn.access",
            "gunicorn.error",
            "uvicorn",
            "uvicorn.access",
            "uvicorn.error",
            "ariadne",
        ]:
            if name not in seen:
                seen.add(name.split(".")[0])
                logging.getLogger(name).handlers = [InterceptHandler()]

        logger.configure(handlers=[{"sink": stdout, "serialize": False}])

        return {
            "bind": self.config.bind,
            "workers": self.config.workers,
            "accesslog": "-",
            "errorlog": "-",
            "worker_class": "uvicorn.workers.UvicornWorker",
            "logger_class": StubbedGunicornLogger
        }


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        message = record.getMessage()
        if record.exc_info:
            etype, _, _ = record.exc_info
            if etype == GraphQLError:
                record.exc_info = None
                message = message.split("\n", 1)[0]
                level = "DEBUG"

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, message)

class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
            c: Config = Config(CONFIG_PATH)
            handler = logging.NullHandler()
            self.error_logger = logging.getLogger("gunicorn.error")
            self.error_logger.addHandler(handler)
            self.access_logger = logging.getLogger("gunicorn.access")
            self.access_logger.addHandler(handler)
            self.error_logger.setLevel(c.logLevel)
            self.access_logger.setLevel(c.logLevel)