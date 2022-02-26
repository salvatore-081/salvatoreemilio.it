from keycloak import KeycloakOpenID, KeycloakAdmin
from os import getenv
import asyncio
from exceptions.base import Unauthorized, BadRequest, Forbidden


class Keycloak:
    def __init__(self) -> None:
        try:
            server_url = getenv(
                "KEYCLOAK_URL", "https://iam.salvatoreemilio.it/auth/")
            realm_name = getenv("KEYCLOAK_REALM_NAME", "se")
            client_id = getenv("KEYCLOAK_CLIENT_ID", "api-auth")
            service_account_client_id = getenv(
                "KEYCLOAK_SERVICE_ACCOUNT_CLIENT_ID", "api-service-account")

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

            self.keycloak_service_account = KeycloakAdmin(
                server_url=server_url,
                client_id=service_account_client_id,
                realm_name=realm_name,
                client_secret_key=service_account_client_secret_key
            )
            asyncio.create_task(
                self.refresh_keycloak_service_account_token(server_url, service_account_client_id, realm_name, service_account_client_secret_key))
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

    async def refresh_keycloak_service_account_token(self, server_url, service_account_client_id, realm_name, service_account_client_secret_key):
        wait_time = 60 * 60 * 24 * 179  # 180 days in seconds minus 1 day for leniency
        await asyncio.sleep(wait_time)
        while True:
            self.keycloak_service_account = KeycloakAdmin(
                server_url=server_url,
                client_id=service_account_client_id,
                realm_name=realm_name,
                client_secret_key=service_account_client_secret_key
            )
            await asyncio.sleep(wait_time)

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

    def check_view_users(self, introspection, email: str) -> None:
        try:
            if email != introspection['email'] and not 'view-users' in introspection['resource_access']['realm-management']['roles']:
                raise
        except Exception:
            raise Forbidden()
