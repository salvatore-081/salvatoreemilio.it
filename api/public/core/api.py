from fastapi import FastAPI, APIRouter
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from state.appState import AppState
from constants.graphql import SCHEMA
from .routers.users import getUsersRouter
from .graphql.query import getQuery


appState = AppState()

api_router = APIRouter()

users_router = getUsersRouter(appState)

api_router.include_router(users_router, prefix="/users", tags=["users"])

app = FastAPI(
    title="salvatoreemilio.it", openapi_url="/openapi.json"
)

app.include_router(api_router, prefix="")

gqlApp = GraphQL(make_executable_schema(
    SCHEMA, getQuery(appState)), keepalive=30)

app.mount("/graphql", gqlApp)

# # Set all CORS enabled origins
# app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
