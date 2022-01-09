from deps.keycloak import Keycloak
from deps.gPRCClient import GPRCClient


class AppState():
    def __init__(self):
        try:
            self.gRPCCLient = GPRCClient()
            self.keycloak = Keycloak()
        except Exception as e:
            raise e

    def select_gPRCClient(self):
        return self.gRPCCLient

    def select_keycloak(self):
        return self.keycloak
