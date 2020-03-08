from typing import *
from sqqrobot.rtypes.messages import Message


class MessagePipe:
    class HandlerLine:
        def __init__(self, handler: Callable):
            self.handler = handler
            self.next = None

    def __init__(self):
        self.pipe = None

    def add_handler(self, handler: Callable):
        if not self.pipe:
            self.pipe = MessagePipe.HandlerLine(handler)
        else:
            pipe_header = MessagePipe.HandlerLine(handler)
            pipe_header.next = self.pipe
            self.pipe = pipe_header

    def flow(self, message: Message):
        pointer: MessagePipe.HandlerLine = self.pipe
        while pointer:
            message = pointer.handler(message)
            if not message:
                return
            pointer = pointer.next
