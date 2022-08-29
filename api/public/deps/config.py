from json import load
from multiprocessing import cpu_count

class GRPCServerConfig():
    host: str
    port: str
    
    def __init__(self, gRPCServerConfig: dict[str, str]) -> None:
        for k in gRPCServerConfig:
            self.__setattr__(k, gRPCServerConfig[k])

class KeycloakConfig():
    realm: str
    url: str
    clientId: str
    serviceAccountClientId: str

    def __init__(self, keycloakConfig: dict[str, str]) -> None:
        for k in keycloakConfig:
            self.__setattr__(k, keycloakConfig[k])

class Config():
    logLevel: str
    workers: int
    bind: str
    gRPCServer: GRPCServerConfig
    keycloak: KeycloakConfig

    def __init__(self, path: str) -> None:
        try:
            with open(path) as c:
                config = load(c)
                self.logLevel = config["logLevel"].upper() if self.checkLogLevel(config["logLevel"]) else "DEBUG"
                self.workers = config["workers"] if (config["workers"] is not None and config["workers"].isnumeric() and int(config["workers"]) > 0) else ((cpu_count() * 2) + 1)
                self.bind = f"0.0.0.0:{config['port'] if config['port'].isnumeric() else '14200'}"
                self.gRPCServer = GRPCServerConfig(config["gRPCServer"])
                self.keycloak = KeycloakConfig(config["keycloak"])
        except Exception as e:
            raise e
    
    def checkLogLevel(self, level: str):
        return level.upper() in ['CRITICAL','FATAL','ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG']