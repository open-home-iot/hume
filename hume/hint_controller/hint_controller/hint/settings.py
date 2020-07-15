from . import hint_req_lib


# Override to assign a mock/simulator module as the implementer of outgoing
# HINT requests.
# NOTE! Had to (?) create a function to return the bloody value since the module
# using it uses the from x import y notation, which creates a local symbol of
# this module variable. When I then tried to override this mod var the
# application module had its local symbol left and was unaffected. By putting
# it into a function it seems to attempt and reload the module variable instead.
_hint_req_mod = hint_req_lib


def req_mod():
    """
    Returns the HINT request module.
    :return:
    """
    return _hint_req_mod
