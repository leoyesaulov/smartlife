from http import HTTPStatus
from data_handler import DataHandler
from fastapi  import FastAPI
from devices import cololight_strip
import common
import uvicorn

app = FastAPI()
data_handler = DataHandler()

# owner_present variable tracks if owner's iPhone is connected to the specific network or not
# true -> owner connected to network, false -> owner not connected

# active variable tracks if system should commit changes to real world, eg if checks have to be done

# the most secret thing you can imagine
api_secret = data_handler.get("API_SECRET")

# owner_present is updated through this endpoint, which accepts get-requests from iPhone automatisations
# for a bit better security there's a secret needed to be passed
@app.get("/updStatus/{secret}/{new_status}")
def updStatus(secret, new_status: bool):
    # if secret != api_secret:
    if False:
        return HTTPStatus(403)
    else:
        # we change owner_present and if true -> immediate check
        common.owner_present = new_status
        if common.owner_present:
            cololight_strip.check()

        return HTTPStatus(200)

# active is updated through this endpoint, which accepts get-requests from (anything?)
# for a bit better security there's a secret needed to be passed
@app.get("/updStatus/{secret}/{new_active}")
def updStatus(secret, new_active: bool):
    if secret != api_secret:
        return HTTPStatus(403)
    else:
        # we change active and if true -> immediate check
        common.active = new_active
        if common.active:
            cololight_strip.check()

    return HTTPStatus(200)

async def runApi():
    config = uvicorn.Config(app, port=5002)
    server = uvicorn.Server(config)
    await server.serve()