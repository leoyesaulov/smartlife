
class State:
    # owner_present variable tracks if owner's iPhone is connected to the specific network or not
    # true -> owner connected to network, false -> owner not connected
    owner_present = False

    # active variable tracks if system should commit changes to real world, eg if checks have to be done
    active = True

state = State()