from deps.config import Config
from deps.keycloak import Keycloak
from deps.gRPCClient import GRPCClient


class AppState():
    def __init__(self, config: Config):
        try:
            self.config: Config = config
            self.gRPCCLient = GRPCClient(self.config.gRPCServer)
            self.keycloak = Keycloak(self.config.keycloak)
        except Exception as e:
            raise e

    def select_gPRCClient(self):
        return self.gRPCCLient

    def select_keycloak(self):
        return self.keycloak
