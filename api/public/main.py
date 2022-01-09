from fastapi import FastAPI
import uvicorn
import os
import grpc
import internal_pb2_grpc
import internal_pb2

channel = grpc.insecure_channel('localhost:8080')
stub = internal_pb2_grpc.InternalStub(channel)

feature = stub.GetUser(internal_pb2.GetUserInput(
    email="info@salvatoreemilio.it"))
print("feature", feature)


app = FastAPI(
    title="salvatoreemilio.it", openapi_url="/openapi.json"
)

if __name__ == "__main__":
    uvicorn.run("core.api:app", host='0.0.0.0', port=int(
        os.getenv("PORT", default=14020)), workers=4, lifespan="on")
