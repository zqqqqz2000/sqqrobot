from typing import *
from sqqrobot import qqbot
from sqqrobot.rtypes.errors import FilterInitException


class Filter:
    def __init__(self):
        raise FilterInitException('The Filter can\'t be init, please use its static function as decorator.')


class GroupsFilter(Filter):
    @staticmethod
    def all_groups():
        """
        allow all the groups
        """
        def _all_groups(func: Callable[[qqbot.GroupMessage], Optional[qqbot.Message]]):
            def inner(message: qqbot.GroupMessage) -> Optional[qqbot.Message]:
                if not isinstance(message, qqbot.GroupMessage):
                    return message
                return func(message)
            return inner
        return _all_groups

    @staticmethod
    def allow_groups(groups_id: Collection[str]):
        """
        only allow to handle groups in parameter groups_id (group_id must be str)
        :param groups_id: a Collection contains all the group_id will handled by this function
        """
        def _allow_groups(func: Callable[[qqbot.GroupMessage], Optional[qqbot.Message]]):
            def inner(message: qqbot.GroupMessage) -> Optional[qqbot.Message]:
                if not isinstance(message, qqbot.GroupMessage):
                    return message
                if message.group_id not in groups_id:
                    return message
                return func(message)
            return inner
        return _allow_groups

    @staticmethod
    def denied_groups(groups_id: Collection[str]):
        """
        handle group messages except group_id in parameter groups_id
        :param groups_id: a Collection contains all the group_id will not handled by this function
        """
        def _denied_groups(func: Callable[[qqbot.GroupMessage], Optional[qqbot.Message]]):
            def inner(message: qqbot.GroupMessage) -> Optional[qqbot.Message]:
                if not isinstance(message, qqbot.GroupMessage):
                    return message
                if message.group_id in groups_id:
                    return message
                return func(message)
            return inner
        return _denied_groups


class PrivateMessageFilter(Filter):
    @staticmethod
    def all_message():
        """
        receive all the private message
        """
        def _all_message(func: Callable[[qqbot.PrivateMessage], Optional[qqbot.Message]]):
            def inner(message: qqbot.PrivateMessage) -> Optional[qqbot.Message]:
                if not isinstance(message, qqbot.PrivateMessage):
                    return message
                return func(message)
            return inner
        return _all_message

    @staticmethod
    def allow_private_message(qqs: Collection[str]):
        """
        only receive messages from qq in parameter qqs(all the qq is str)
        :param qqs: Collection contains all the qq allow to be handled by this function
        """
        def _allow_private_message(func: Callable[[qqbot.PrivateMessage], Optional[qqbot.Message]]):
            def inner(message: qqbot.PrivateMessage) -> Optional[qqbot.Message]:
                if not isinstance(message, qqbot.PrivateMessage):
                    return message
                if message.qq in qqs:
                    return message
                return func(message)
            return inner
        return _allow_private_message

    @staticmethod
    def denied_private_message(qqs: Collection):
        """
         only receive messages from qq in parameter qqs(all the qq is str)
         :param qqs: Collection contains all the qq not allow to be handled by this function
         """
        def _denied_private_message(func: Callable[[qqbot.PrivateMessage], Optional[qqbot.Message]]):
            def inner(message: qqbot.PrivateMessage) -> Optional[qqbot.Message]:
                if isinstance(message, qqbot.PrivateMessage):
                    return message
                if message.qq in qqs:
                    return message
                return func(message)
            return inner
        return _denied_private_message


class SelfDefineFilter(Filter):
    @staticmethod
    def message_filter(filter_func: Callable[[qqbot.Message], bool]):
        """
        filter message by user defined function, only if filter_func(message) returns True
        :param filter_func: filter_func: Callable[[message], bool]
        """
        def _message_filter(func: Callable[[qqbot.Message], Optional[qqbot.Message]]):
            def inner(message: qqbot.Message) -> Optional[qqbot.Message]:
                if not filter_func(message):
                    return message
                return func(message)
            return inner
        return _message_filter
