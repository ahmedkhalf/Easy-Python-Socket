import socket
import threading

# Constants for start()
SERVER = 0
CLIENT = 1

_network_class = None # Either _server or _client class
_exposed_functions = {}

_start_args = {
    'host': 'localhost',
    'port': 55555,
}

# --------------- #
# Private Classes #
# --------------- #

class _server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_list = {}

    def get_clients(self):
        id = 0
        while True:
            c, addr = self.socket.accept()
            self.client_list[id] = (c, addr)
            id += 1

    def start(self, _start_args):
        self.socket.bind((_start_args['host'], _start_args['port']))
        self.socket.listen(10)


class _client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, _start_args):
        self.socket.connect((_start_args['host'], _start_args['port']))

# ---------------- #
# Public Functions #
# ---------------- #

def start(mode, **kwargs):
    _start_args.update(kwargs)

    global _network_class
    if mode == SERVER:
        _network_class = _server()
        _network_class.start(_start_args)
    else:
        _network_class = _client()
        _network_class.start(_start_args)


def getSocketType():
    # Returns SERVER, CLIENT, or None
    if _network_class is not None:
        if type(_network_class) == _client:
            return CLIENT
        return SERVER


def expose(name_or_function=None):
    # Deal with '@spc.expose()' - treat as '@spc.expose'
    if name_or_function is None:
        return expose

    if type(name_or_function) == str:   # Called as '@spc.expose("my_name")'
        name = name_or_function

        def decorator(function):
            _expose(name, function)
            return function
        return decorator
    else:
        function = name_or_function
        _expose(function.__name__, function)
        return function

# ----------------- #
# Private Functions #
# ----------------- #

def _expose(name, function):
    msg = 'Already exposed function with name "%s"' % name
    assert name not in _exposed_functions, msg
    _exposed_functions[name] = function
