from . import device_req_lib


# Override this module to insert mocking mods/simulators. It will make sure
# outbound device traffic gets sent via the set module's implementation of the
# device interface.
device_req_mod = device_req_lib
