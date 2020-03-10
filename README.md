# SQQRobot

sqqrobot is a qq(Tencent qq) robot python api, based on [CQA](https://cqp.cc/) and its plugin [CQSocket](https://github.com/yukixz/cqsocketapi), CQSocket has been attached in project root `org.dazzyd.cqsocketapi.cpk`.

## Usage

First, import SQQRobot.

```python
from sqqrobot.qqbot import QQbot
```

### Message Handler

Handler is a kind of function which will be called when the server received a message.

User can define his own message handler function easily by using **decorator**```@QQbot.as_pipe```.

###### Example

```python
@QQbot.as_pipe
def handler(message: QQbot.Message) -> Optional[QQbot.Message]:
    ...
```

The handler function is not parallel, the way to handle a message like water(message) flows through pipe(handler functions), if one of the handler function returns `None`. This message will treat as handled, or else the return of the handler function will be handled by next handler function.

###### Example

```python
@QQbot.as_pipe
def handler1(message):
    return message

@QQbot.as_pipe
def handler2(message):
    return None

@QQbot.as_pipe
def handler3(message):
    return message
```

when the service received a message. The message will handled by following sequence.

handler1==>handler2=x>handler3

### Handler Filter

Filters is a series of decorator which allows user assign which handler will handle which kind of message.

import filters.

```python
from sqqrobot import filters
```

all filters.

```python
class GroupsFilter(Filter):
    @staticmethod
    def all_groups():
        """
        allow all the groups
        """
        ...

    @staticmethod
    def allow_groups(groups_id: Collection[str]):
        """
        only allow to handle groups in parameter groups_id (group_id must be str)
        :param groups_id: a Collection contains all the group_id will handled by this function
        """
        ...

    @staticmethod
    def denied_groups(groups_id: Collection[str]):
        """
        handle group messages except group_id in parameter groups_id
        :param groups_id: a Collection contains all the group_id will not handled by this function
        """
        ...


class PrivateMessageFilter(Filter):
    @staticmethod
    def all_message():
        """
        receive all the private message
        """
        ...

    @staticmethod
    def allow_private_message(qqs: Collection[str]):
        """
        only receive messages from qq in parameter qqs(all the qq is str)
        :param qqs: Collection contains all the qq allow to be handled by this function
        """
        ...

    @staticmethod
    def denied_private_message(qqs: Collection):
        """
         only receive messages from qq in parameter qqs(all the qq is str)
         :param qqs: Collection contains all the qq not allow to be handled by this function
         """
        ...


class SelfDefineFilter(Filter):
    @staticmethod
    def message_filter(filter_func: Callable[[qqbot.Message], bool]):
        """
        filter message by user defined function, only if filter_func(message) returns True
        :param filter_func: filter_func: Callable[[message], bool]
        """
        ...
```

###### Example

```python
@QQbot.as_pipe
@filters.PrivateMessageFilter.all_message()
def private_handler(message: qqbot.PrivateMessage) -> Optional[qqbot.Message]:
    ...
```

In this case, function private_handler will only handle all the private message.

### Message Types

SQQRobot assembled five message types in ```sqqrobot.qqbot```. It will be taken as argument `message` of the handler function.

```python
class PrivateMessage(Message):
    def __init__(self, qq: str, message: str):
        ...

class GroupMessage(Message):
    def __init__(self, group_id: str, message: str, qq: str = ''):
        ...


class DiscussMessage(Message):
    def __init__(self, discuss_id: str, message: str, qq: str=''):
        ...


class GroupMemberDecrease(Message):
    def __init__(self, group_id: str, qq: str, operated_qq: str):
        ...


class GroupMemberIncrease(Message):
    def __init__(self, group_id: str, qq: str, operated_qq: str):
        ...
```

**First three message type can be both treat as receiving type and sending type**

###### Example

```python
message_back = qqbot.GroupMessage(group_id, 'Hello world.')
bot.send_message(message_back)
```

## Quick Start

Plugin CQSocket must be loaded by CQA.

```python
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
```

### Result

Private conversation

![image-20200308222239772](README.assets/image-20200308222239772.png)

Group conversation

![image-20200308222623027](README.assets/image-20200308222623027.png)