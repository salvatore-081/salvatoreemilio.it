from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import get_introspection_query, build_client_schema, print_schema
from os import getenv, linesep
from graphql.language.printer import Strings
import requests
from constants.graphql import *
import json

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

    def get_schema(self):
        try:
            res = requests.post(
                self.url, json={"query": get_introspection_query()}, headers={"Content-Type": "application/json"})
            s = json.loads(res.text)
            return "".join([s for s in print_schema(build_client_schema(s["data"])).replace("#", "").strip().splitlines(True) if s.strip()]).replace("}", "}\n")
        except Exception as e:
            raise e

    async def get_user(self, email: str):
        try:
            res = await self.session.execute_async(
                GET_USER, variable_values={"email": email})
            return res
        except Exception as e:
            raise e
