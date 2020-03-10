from sqqrobot.lib.ss import RequestHandle
import socketserver
import threading
from typing import *

import sqqrobot.lib.global_var as global_var
import time
import socket
from sqqrobot.rtypes.messages import *


class QQbot:
    def __init__(self, serve_port: int, qsocket_port: int):
        self._port = serve_port
        self.pipe = global_var.pipe
        self._qsocket_port = qsocket_port

    def send_message(self, message: Message):
        skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = str(message).encode()
        addr = ('127.0.0.1', self._qsocket_port)
        skt.sendto(msg, addr)
        skt.close()

    def _heart_beat(self):
        while True:
            skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            msg = f'ClientHello {self._port}'.encode()
            addr = ('127.0.0.1', self._qsocket_port)
            skt.sendto(msg, addr)
            skt.close()
            time.sleep(30)

    @staticmethod
    def as_pipe(pipe_func: Callable):
        global_var.pipe.add_handler(pipe_func)

    def serve(self):
        s = threading.Thread(target=self._heart_beat)
        s.start()
        laddr = "127.0.0.1", self._port
        udpserver = socketserver.UDPServer(laddr, RequestHandle)
        udpserver.serve_forever()
