from fastapi import APIRouter
from deps.gql import GQLClient


def getUserRouter(gqlClient: GQLClient):
    router = APIRouter()

    @router.get("/{email}")
    async def get_user(email: str):
        return await gqlClient.get_user(email=email)

    return router
