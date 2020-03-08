import base64


class Message:
    def _message_encoder(self, message) -> str:
        return base64.b64encode(message.encode('GB18030')).decode()


class PrivateMessage(Message):
    def __init__(self, qq: str, message: str):
        self.qq: str = qq
        self.message: str = message

    def __str__(self):
        return f'PrivateMessage {self.qq} {self._message_encoder(self.message)}'


class GroupMessage(Message):
    def __init__(self, group_id: str, message: str, qq: str = ''):
        self.group_id: str = group_id
        self.qq: str = qq
        self.message: str = message

    def __str__(self):
        return f'GroupMessage {self.group_id} {self._message_encoder(self.message)}'


class DiscussMessage(Message):
    def __init__(self, discuss_id: str, message: str, qq: str=''):
        self.discuss_id: str = discuss_id
        self.qq: str = qq
        self.message: str = message

    def __str__(self):
        return f'DiscussMessage {self.discuss_id} {self._message_encoder(self.message)}'


class GroupMemberDecrease(Message):
    def __init__(self, group_id: str, qq: str, operated_qq: str):
        self.group_id: str = group_id
        self.qq: str = qq
        self.operated_qq: str = operated_qq


class GroupMemberIncrease(Message):
    def __init__(self, group_id: str, qq: str, operated_qq: str):
        self.group_id: str = group_id
        self.qq: str = qq
        self.operated_qq: str = operated_qq
