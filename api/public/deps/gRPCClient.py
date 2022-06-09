from grpc.aio import insecure_channel
from deps.config import GRPCServerConfig
from proto.internal_pb2_grpc import InternalStub
from proto.internal_pb2 import GetUserInput, GetUserListInput, UpdateUserInput, UpdateUserInputPayload, WatchUserInput


class GRPCClient():
    def __init__(self, config: GRPCServerConfig) -> None:
        try:
            self.config = config
            self.url = f"{self.config.host}:{self.config.port}"
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

    async def get_user_list(self):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                getUserList = await st.GetUserList(GetUserListInput())
                return getUserList
        except Exception as e:
            raise e

    async def add_user(self, user: any):
        try:
            res = {}
            # res = await self.session.execute_async(ADD_USER, variable_values={"input": user.dict()})
            return res
        except Exception as e:
            raise e

    async def update_user(self, email: str, payload: UpdateUserInputPayload):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                updateUser = await st.UpdateUser(UpdateUserInput(email=email, updateUserInputPayload=UpdateUserInputPayload(**payload.dict())))
                return updateUser
        except Exception as e:
            raise e

    async def watch_user(self, email: str):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                async for user in st.WatchUser(WatchUserInput(email=email)):
                    yield user
        except Exception as e:
            raise e