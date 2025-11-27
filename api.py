from http import HTTPStatus
from data_handler import DataHandler
from fastapi  import FastAPI
from devices import cololight_strip
import uvicorn

app = FastAPI()
data_handler = DataHandler()

# status variable tracks if owner's iPhone is connected to the specific network or not
# true -> owner connected to network, false -> owner not connected
status = False

# the most secret thing you can imagine
api_secret = data_handler.get("API_SECRET")

# status is updated through this endpoint, which accepts get-requests from iPhone automatisations
# for a bit better security there's a secret needed to be passed
@app.get("/updStatus/{secret}/{new_status}")
def updStatus(secret, new_status: bool):
    if secret != api_secret:
        return HTTPStatus(403)
    else:
        # we change status and if true -> immediate check
        status = new_status
        if status:
            cololight_strip.check()

    return HTTPStatus(200)

async def runApi():
    config = uvicorn.Config(app, port=5002)
    server = uvicorn.Server(config)
    await server.serve()