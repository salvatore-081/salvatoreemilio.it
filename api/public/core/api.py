from os import getenv
from fastapi import FastAPI, APIRouter
from .routers.users import getUsersRouter
from ariadne import ObjectType, QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from .graphql.query import getQuery
from state.appState import AppState


appState = AppState()

api_router = APIRouter()

users_router = getUsersRouter(appState)

api_router.include_router(users_router, prefix="/users", tags=["users"])

app = FastAPI(
    title="salvatoreemilio.it", openapi_url="/openapi.json"
)

app.include_router(api_router, prefix="")

gqlApp = GraphQL(make_executable_schema(
    appState.select_gqlClient().get_schema(), getQuery()))

app.mount("/graphql/", gqlApp)

# # Set all CORS enabled origins
# app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
