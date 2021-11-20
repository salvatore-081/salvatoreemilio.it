import os
import uvicorn

if __name__ == "__main__":
    uvicorn.run("rest.v1.api:app", host='0.0.0.0', port=os.getenv("PORT", default=14020),
                reload=False, debug=True, workers=2)
