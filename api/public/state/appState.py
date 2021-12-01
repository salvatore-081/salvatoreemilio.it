from deps.gql import GQLClient
from deps.keycloak import Keycloak


class AppState():
    def __init__(self):
        try:
            self.gqlClient = GQLClient()
            self.keycloak = Keycloak()
        except Exception as e:
            raise e

    def select_gqlClient(self):
        return self.gqlClient

    def select_keycloak(self):
        return self.keycloak
