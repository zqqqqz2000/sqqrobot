from sqqrobot.qqbot import QQbot
from sqqrobot import qqbot
from typing import *

bot = QQbot(23333, 11235)


@bot.as_pipe
def private_handler(message: qqbot.PrivateMessage) -> Optional[qqbot.Message]:
    if not isinstance(message, qqbot.PrivateMessage):
        return message
    message_back: qqbot.PrivateMessage = qqbot.PrivateMessage(message.qq,
                                                              f'received private message: {message.message}\n'
                                                              f'from {message.qq}')
    bot.send_message(message_back)


@bot.as_pipe
def group_handler(message: qqbot.GroupMessage) -> Optional[qqbot.Message]:
    if not isinstance(message, qqbot.GroupMessage):
        return message
    message_back = qqbot.GroupMessage(message.group_id, f'received group message: {message.message}\n'
                                                        f'from {message.group_id}')
    bot.send_message(message_back)


if __name__ == '__main__':
    bot.serve()
