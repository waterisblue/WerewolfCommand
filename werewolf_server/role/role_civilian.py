from abc import abstractmethod

from werewolf_server.role.base_role import BaseRole, RoleStatus, RoleChannel
from werewolf_server.utils.i18n import Language


class RoleCivilian(BaseRole):
    def __init__(self):
        self._status = RoleStatus.STATUS_ALIVE
        self._name = Language.get_translation('civilian')
        self._channels =  [RoleChannel.CHANNEL_NORMAL,]

    @property
    def channels(self):
        return self._channels

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def name(self):
        return self._name

    async def night_action(self, member):
        pass

    async def day_action(self, member):
        pass

    async def voting_action(self, member):
        pass