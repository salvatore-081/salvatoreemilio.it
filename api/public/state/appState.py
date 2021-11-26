from deps.gql import GQLClient


class AppState():
    def __init__(self):
        self.gqlClient = GQLClient()

    def select_gqlClient(self):
        return self.gqlClient
