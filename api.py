import grpc
from common import state
from concurrent import futures
from devices import cololight_strip
from data_handler import DataHandler
from protobufs import smartlife_pb2, smartlife_pb2_grpc

data_handler = DataHandler()
RPC_PORT = "5002"

class StatusUpdateServicer(smartlife_pb2_grpc.StateUpdateServicer):
    def StatusUpdate(self, request, context):
        updStatus(request.status)
        return smartlife_pb2.UpdateResponse(success=True)

    def ActiveUpdate(self, request, context):
        updActive(request.active)
        return smartlife_pb2.UpdateResponse(success=True)

    def BrightnessUpdate(self, request, context):
        updBrightness(request.brightness)
        return smartlife_pb2.UpdateResponse(success=True)

# owner_present variable tracks if owner's iPhone is connected to the specific network or not
# true -> owner connected to network, false -> owner not connected

# active variable tracks if system should commit changes to real world, eg if checks have to be done

# ToDo: refactor status variable naming
def updStatus(new_status: bool):
    # we change owner_present and immediate check
    state.owner_present = new_status
    cololight_strip.check()

def updActive(new_active: bool):
    # we change active and if true -> immediate check
    state.service_active = new_active
    if state.service_active:
        cololight_strip.check()

def updBrightness(new_brightness: int):
    cololight_strip.updBrightness(new_brightness)

def runApi():
    rpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    smartlife_pb2_grpc.add_StateUpdateServicer_to_server(
        servicer=StatusUpdateServicer(),
        server=rpc_server
    )
    rpc_server.add_insecure_port(f"localhost:{RPC_PORT}")
    rpc_server.start()
    print(f"RPC server listening on port :{RPC_PORT}")
    rpc_server.wait_for_termination()