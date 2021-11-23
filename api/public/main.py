import os
import uvicorn

if __name__ == "__main__":
    uvicorn.run("core.api:app", host='0.0.0.0', reload=True, port=int(
        os.getenv("PORT", default=14020)), workers=4)
