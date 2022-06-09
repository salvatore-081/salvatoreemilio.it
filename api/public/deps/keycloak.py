from keycloak import KeycloakOpenID, KeycloakAdmin
from os import getenv
from deps.config import KeycloakConfig
from exceptions.base import Unauthorized, BadRequest, Forbidden
import threading


class Keycloak:
    def __init__(self, config: KeycloakConfig) -> None:
        try:
            self.config: KeycloakConfig = config
            server_url = config.url
            realm_name = self.config.realm
            client_id = self.config.clientId
            service_account_client_id = self.config.serviceAccountClientId

            client_secret_key = getenv("KEYCLOAK_CLIENT_SECRET_KEY")
            if client_secret_key is None:
                raise Exception(
                    "Error reading KEYCLOAK_CLIENT_SECRET_KEY environment variable")

            service_account_client_secret_key = getenv(
                "KEYCLOAK_SERVICE_ACCOUNT_CLIENT_SECRET_KEY")
            if service_account_client_secret_key is None:
                raise Exception(
                    "Error reading KEYCLOAK_SERVICE_ACCOUNT_CLIENT_SECRET_KEY environment variable")

            self.keycloak_openid = KeycloakOpenID(
                server_url=server_url,
                client_id=client_id,
                realm_name=realm_name,
                client_secret_key=client_secret_key)
            self.keycloak_service_account(
                server_url, service_account_client_id, realm_name, service_account_client_secret_key)
        except Exception as e:
            raise e

    def login(self, username: str, password: str, totp: str):
        try:
            return self.keycloak_openid.token(username, password, totp=totp)
        except Exception as e:
            raise e

    def logout(self, refresh_token: str):
        try:
            return self.keycloak_openid.logout(refresh_token)
        except Exception as e:
            raise e

    def keycloak_service_account(self, server_url, service_account_client_id, realm_name, service_account_client_secret_key):
        self.keycloak_service_account = KeycloakAdmin(
            server_url=server_url,
            client_id=service_account_client_id,
            realm_name=realm_name,
            client_secret_key=service_account_client_secret_key
        )
        wait_time = 60 * 60 * 24 * 59  # 60 days in seconds minus 1 day for leniency
        t = threading.Timer(
            wait_time, self.keycloak_service_account, args=[server_url, service_account_client_id, realm_name, service_account_client_secret_key])
        t.daemon = True
        t.start()

    def introspect_token(self, token: str) -> any:
        try:
            introspection = self.keycloak_openid.introspect(token=token)
            return introspection
        except Exception as e:
            raise e

    def check_active(self, introspection) -> None:
        try:
            if not introspection["active"]:
                raise Unauthorized()
        except KeyError:
            raise BadRequest()
        except Exception as e:
            raise e

    def check_view_users(self, introspection: any, email: str) -> None:
        try:
            if email != introspection['email'] and not "admin" in introspection['realm_access']['roles']:
                raise
        except Exception:
            raise Forbidden()

    def check_manage_users(self, introspection: any, email: str) -> None:
        try:
            if email != introspection['email'] and not "admin" in introspection['realm_access']['roles']:
                raise
        except Exception:
            raise Forbidden()
