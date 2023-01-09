from fastapi import FastAPI, Request
import uvicorn
from tools.redis_client import RedisClient
import json
from tools.errors import *
from tools.validation import validate_parameters

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/get")
async def get_value(request: Request):
    try:
        data = await request.json()
    except (Exception,):
        return json_error

    valid_request = validate_parameters(parameters=[
        {"key": "key",
         "value": data.get("key")}
    ], requiredFields=["key"])

    if valid_request.get("success") is False:
        return valid_request

    try:
        result = RedisClient.get(str(data.get("key")))
    except (Exception,):
        return key_error

    return result


@app.post("/set")
async def set_value(request: Request):
    try:
        data = await request.json()
    except (Exception,):
        return json_error

    valid_request = validate_parameters(parameters=[
        {"key": "key",
         "value": data.get("key")},
        {"key": "value",
         "value": data.get("value")}
    ], requiredFields=["key"])

    if valid_request.get("success") is False:
        return valid_request

    try:
        value = json.dumps(data.get("value"))
    except (Exception,):
        pass

    return RedisClient.set(data.get("key"), value)


uvicorn.run(app, host="0.0.0.0", port=5000)
