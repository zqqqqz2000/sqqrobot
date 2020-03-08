import socketserver
from sqqrobot.rtypes.messages import *
import sqqrobot.lib.global_var as global_var
from sqqrobot.rtypes.pipe import MessagePipe


class RequestHandle(socketserver.BaseRequestHandler):
    def setup(self):
        super().setup()

    @staticmethod
    def message_decoder(message: bytes) -> str:
        message: str = base64.b64decode(message).decode('GB18030', errors='ignore')
        return message

    def handle(self):
        super().handle()
        pipe: MessagePipe = global_var.pipe
        context, sk = self.request
        if context == b'ServerHello':
            return
        type_ = context.split(b' ')[0]
        if type_ == b'PrivateMessage':
            type_, qq, message = context.split(b' ')
            pipe.flow(PrivateMessage(qq=qq.decode(), message=self.message_decoder(message)))
        elif type_ == b'GroupMessage':
            type_, group_id, qq, message = context.split(b' ')
            pipe.flow(GroupMessage(qq=qq.decode(), group_id=group_id.decode(), message=self.message_decoder(message)))
        elif type_ == b'DiscussMessage':
            type_, discuss_id, qq, message = context.split(b' ')
            pipe.flow(DiscussMessage(qq=qq.decode(), discuss_id=discuss_id.decode(), message=self.message_decoder(message)))
        elif type_ == b'GroupMemberDecrease':
            type_, group_id, qq, operated_qq = context.split(b' ')
            pipe.flow(GroupMemberDecrease(qq=qq.decode(), group_id=group_id.decode(), operated_qq=operated_qq.decode))
        elif type_ == b'GroupMemberIncrease':
            type_, group_id, qq, operated_qq = context.split(b' ')
            pipe.flow(GroupMemberIncrease(qq=qq.decode(), group_id=group_id.decode(), operated_qq=operated_qq.decode))

    def finish(self):
        super().finish()
