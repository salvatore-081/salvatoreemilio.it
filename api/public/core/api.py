from os import getenv
from fastapi import FastAPI, APIRouter
from deps.gql import GQLClient
from .routers.users import getUserRouter


gqlClient = GQLClient(
    f"http://{getenv('INTERNAL_API_HOST', 'internal-api')}:{getenv('INTERNAL_API_PORT', '14010')}/")

api_router = APIRouter()
users_router = getUserRouter(gqlClient)

api_router.include_router(users_router, prefix="/users", tags=["users"])

app = FastAPI(
    title="salvatoreemilio.it", openapi_url="/openapi.json"
)

# # Set all CORS enabled origins
# app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

app.include_router(api_router, prefix="")
