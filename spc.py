import socket
import threading

# Constants for start()
SERVER = 0
CLIENT = 1

_start_args = {
    'host': 'localhost',
    'port': 55555,
}

class Server:
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


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, _start_args):
        self.socket.bind((_start_args['host'], _start_args['port']))
        self.socket.listen(10)


def start(mode, **kwargs):
    _start_args.update(kwargs)
    
    if mode == SERVER:
        server = Server()
        server.start(_start_args)
    else:
        client = Client()
        client.start(_start_args)
