import os
import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="salvatoreemilio.it", openapi_url="/openapi.json"
)

if __name__ == "__main__":
    uvicorn.run("core.api:app", host='0.0.0.0', port=int(
        os.getenv("PORT", default=14020)), workers=4, lifespan="on")
