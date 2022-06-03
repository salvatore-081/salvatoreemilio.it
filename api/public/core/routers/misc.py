from fastapi import APIRouter, Request
from models.misc import WhatsMyIp


def getMiscRouter():
    router = APIRouter()

    @router.get("/whatsmyip", 
    response_model=WhatsMyIp, response_model_exclude_none=True)
    async def get_whats_my_ip(request: Request):
        return {"ip": request.headers.get("x-forwarded-for").split(", ")[0]}

    return router