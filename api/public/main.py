import uvicorn

if __name__ == "__main__":
    uvicorn.run("rest.v1.api:app", host='0.0.0.0', port=4557,
                reload=True, debug=True, workers=3)
