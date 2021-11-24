from fastapi import APIRouter
from starlette.responses import JSONResponse
from deps.gql import GQLClient
from models.user import User


def getUserRouter(gqlClient: GQLClient):
    router = APIRouter()

    @router.get("/{email}", response_model=User)
    async def get_user(email: str):
        try:
            r = await gqlClient.get_user(email=email)
            if not r['getUser']:
                return JSONResponse(
                    status_code=404,
                    content={"message": f"{email} not found"}
                )
            else:
                return r['getUser']
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"message": "unexpected error", "debug": str(e)}
            )

    return router
