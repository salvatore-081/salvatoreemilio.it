from json import load
from multiprocessing import cpu_count

class GRPCServerConfig():
    host: str
    port: str
    
    def __init__(self, gRPCServerConfig: dict[str, str]) -> None:
        for k in gRPCServerConfig:
            self.__setattr__(k, gRPCServerConfig[k])

class GunicornConfig():
    port: str

    def __init__(self, gunicornConfig: dict[str, str]) -> None:
        for k in gunicornConfig:
            self.__setattr__(k, gunicornConfig[k])

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
    gunicorn: GunicornConfig
    keycloak: KeycloakConfig

    def __init__(self, path: str) -> None:
        try:
            with open(path) as c:
                config = load(c)
                self.logLevel = config["logLevel"].upper() if self.checkLogLevel(config["logLevel"]) else "DEBUG"
                self.workers = config["workers"] if (config["workers"] is not None and config["workers"].isnumeric() and int(config["workers"]) > 0) else ((cpu_count() * 2) + 1)
                self.bind = f"0.0.0.0:{config['port'] if config['port'].isnumeric() else '14300'}"
                self.gRPCServer = GRPCServerConfig(config["gRPCServer"])
                self.gunicorn = GunicornConfig(config["gunicorn"])
                self.keycloak = KeycloakConfig(config["keycloak"])
        except Exception as e:
            raise e
    
    def checkLogLevel(self, level: str):
        return level.upper() in ['CRITICAL','FATAL','ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG']