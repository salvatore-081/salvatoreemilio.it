from fastapi import APIRouter

from .endpoints import items

from fastapi import FastAPI
# from starlette.middleware.cors import CORSMiddleware

# from rest.v1.api import api_router

api_router = APIRouter()
api_router.include_router(items.router, prefix="/test", tags=["test"])

app = FastAPI(
    title="salvatoreemilio", openapi_url="/openapi.json"
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
