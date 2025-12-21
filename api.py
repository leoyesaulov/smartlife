from http import HTTPStatus
from common import state
from data_handler import DataHandler
from fastapi  import FastAPI
from devices import cololight_strip
import uvicorn
from pydantic import BaseModel

app = FastAPI()
data_handler = DataHandler()

# owner_present variable tracks if owner's iPhone is connected to the specific network or not
# true -> owner connected to network, false -> owner not connected

# active variable tracks if system should commit changes to real world, eg if checks have to be done

# the most secret thing you can imagine
api_secret = data_handler.get("API_SECRET")

# pydantic class for status and active variable change apis to sanitize input
class BoolUpdateRequestModel(BaseModel):
    secret: str
    new_value: bool


# owner_present is updated through this endpoint, which accepts get-requests from iPhone automatisations
# for a bit better security there's a secret needed to be passed
@app.post("/updStatus/")
def updStatus(request: BoolUpdateRequestModel):
    if request.secret != api_secret:
        return HTTPStatus(403)
    else:
        # we change owner_present and immediate check
        state.owner_present = request.new_value
        cololight_strip.check()
        return HTTPStatus(200)

# active is updated through this endpoint, which accepts get-requests from (anything?)
# for a bit better security there's a secret needed to be passed
@app.post("/updActive/")
def updActive(request: BoolUpdateRequestModel):
    if request.secret != api_secret:
        return HTTPStatus(403)
    else:
        # we change active and if true -> immediate check
        state.active = request.new_value
        if state.active:
            cololight_strip.check()
        return HTTPStatus(200)

async def runApi():
    config = uvicorn.Config(app, port=5002)
    server = uvicorn.Server(config)
    await server.serve()