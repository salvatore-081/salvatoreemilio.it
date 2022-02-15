from os import getenv
from grpc.aio import insecure_channel
from internal_pb2_grpc import InternalStub
from internal_pb2 import GetUserInput


class GPRCClient():
    def __init__(self) -> None:
        try:
            self.url = f"{getenv('INTERNAL_API_HOST', 'internal-api')}:{getenv('INTERNAL_API_PORT', '14010')}"
        except Exception as e:
            raise e

    async def get_user(self, email: str):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                getUser = await st.GetUser(GetUserInput(email=email))
                return getUser
        except Exception as e:
            raise e

    async def add_user(self, user: any):
        try:
            res = {}
            # res = await self.session.execute_async(ADD_USER, variable_values={"input": user.dict()})
            return res
        except Exception as e:
            raise e
