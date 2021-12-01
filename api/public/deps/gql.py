from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from os import getenv

from models.user import User
from constants.graphql import *


class GQLClient():
    def __init__(self) -> None:
        try:
            self.url = f"http://{getenv('INTERNAL_API_HOST', 'internal-api')}:{getenv('INTERNAL_API_PORT', '14010')}/"
            self.session = Client(transport=AIOHTTPTransport(
                url=self.url), fetch_schema_from_transport=True)
        except Exception as e:
            raise e

    async def get_user(self, email: str):
        try:
            res = await self.session.execute_async(GET_USER, variable_values={"email": email})
            return res
        except Exception as e:
            raise e

    async def add_user(self, user: User):
        try:
            res = await self.session.execute_async(ADD_USER, variable_values={"input": user.dict()})
            return res
        except Exception as e:
            raise e
