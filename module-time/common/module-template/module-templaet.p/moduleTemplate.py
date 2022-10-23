from glob import glob
from fastapi import Body, FastAPI, Request
from starlette import status
from starlette.responses import Response, HTMLResponse
import uvicorn
import requests

__clock_port = 3000 

app = FastAPI()

__module_id = ""

def __createGet(route, callback):
    @app.get(route)
    def _(request: Request):
        return callback(request.query_params._dict)

def __createPost(route, callback):
    @app.post(route)
    async def _(payload: dict = Body(...)):
        return callback(payload)

def __createDelete(route, callback):
    @app.delete(route)
    def _(request: Request):
        return callback(request.query_params._dict)

def __createPut(route, callback):
    @app.put(route)
    def _(payload: dict = Body(...)):
        return callback(payload)

def init(_port, _module_id, *params):
    global __module_id
    __module_id = _module_id
    for param in params[0]: 
        if(param[0] == 'post'): 
            __createPost(param[1], param[2])
        
        if(param[0] == 'get'): 
            __createGet(param[1], param[2])

        if(param[0] == 'put'): 
            __createPut(param[1], param[2])

        if(param[0] == 'delete'): 
            __createDelete(param[1], param[2])

    # send get to localhost:3000/register?service_id={module-id}&port={port}
    requests.get("http://localhost:%d/register?service_id=%s&port=%d" % (__clock_port, __module_id, _port))
    uvicorn.run(app, host="localhost", port=_port)

def createEvent(time):
    # send get to localhost:3000/new-event?event-time={time}
    requests.get("http://localhost:%d/new-event?event_time=%d" % (__clock_port, time))

def readyToEvent():
    requests.get("http://localhost:%d/ready-for-event?service_id=%s" % (__clock_port, __module_id))
    # send get to localhost:3000/ready-for-event?service_id={module-id}

# if __name__ == "__main__":
    # uvicorn.run(app, host="localhost", port=8000)