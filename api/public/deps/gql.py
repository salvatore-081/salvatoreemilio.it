from fastapi.encoders import jsonable_encoder
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

GET_USER = gql(
    """
    query getUser($email: String!){
        getUser(email: $email){
            email
            name
            surname
            phoneNumber
            currentLocation
        }
    }
    """
)


class GQLClient():
    def __init__(self, host: str) -> None:
        self.client = Client(transport=AIOHTTPTransport(
            url=host), fetch_schema_from_transport=True)

    async def get_user(self, email: str):
        res = await self.client.execute_async(GET_USER, jsonable_encoder({"email": email}))
        return res
