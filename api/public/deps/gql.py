from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import get_introspection_query, build_client_schema

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

    async def get_schema(self):
        try:
            document = gql(get_introspection_query(descriptions=True))
            res = await self.client.execute_async(document)
            return build_client_schema(res)
        except Exception as e:
            raise e

    async def get_user(self, email: str):
        try:
            res = await self.client.execute_async(
                GET_USER, variable_values={"email": email})
            return res
        except Exception as e:
            raise e
