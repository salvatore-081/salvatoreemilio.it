from pydantic import BaseModel


class WhatsMyIp(BaseModel):
    ip: str