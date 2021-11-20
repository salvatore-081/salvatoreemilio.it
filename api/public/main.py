import os
import uvicorn

if __name__ == "__main__":
    uvicorn.run("rest.v1.api:app", host='0.0.0.0', port=int(
        os.getenv("PORT", default=14020)), workers=2)
