from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from os import getenv

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
    def __init__(self) -> None:
        self.url = f"http://{getenv('INTERNAL_API_HOST', 'internal-api')}:{getenv('INTERNAL_API_PORT', '14010')}/"
        self.session = Client(transport=AIOHTTPTransport(
            url=self.url), fetch_schema_from_transport=True)

    async def get_user(self, email: str):
        try:
            res = await self.session.execute_async(GET_USER, variable_values={"email": email})
            return res
        except Exception as e:
            raise e
