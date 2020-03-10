from sqqrobot.qqbot import QQbot
from sqqrobot import qqbot
from sqqrobot import filters
from typing import *

# serve port is the port this service will listening
# the qsocket port is the listening port of CQSocket, default is 11235
bot = QQbot(serve_port=23333, qsocket_port=11235)


# handle all the private message
@QQbot.as_pipe
@filters.PrivateMessageFilter.all_message()
def private_handler(message: qqbot.PrivateMessage) -> Optional[qqbot.Message]:
    message_back = qqbot.PrivateMessage(message.qq,
                                        f'received private message: {message.message}\n'
                                        f'from {message.qq}')
    bot.send_message(message_back)
    return


# will handle only the group which id is 23333333
@QQbot.as_pipe
@filters.GroupsFilter.allow_groups(['23333333'])
def group_handler(message: qqbot.GroupMessage) -> Optional[qqbot.Message]:
    message_back = qqbot.GroupMessage(message.group_id,
                                      f'received group message: {message.message}\n'
                                      f'from {message.group_id}')
    bot.send_message(message_back)
    return


if __name__ == '__main__':
    # please execute bot.serve() only after loaded all the handler function you defined.
    bot.serve()
