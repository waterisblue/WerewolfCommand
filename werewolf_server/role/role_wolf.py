from werewolf_server.role.base_role import BaseRole, RoleStatus, RoleChannel, NightPriority, Clamp
from werewolf_server.utils.i18n import Language


class RoleWolf(BaseRole):
    def __init__(self):
        self._status = RoleStatus.STATUS_ALIVE
        self._name = Language.get_translation('wolf')
        self._channels = [RoleChannel.CHANNEL_NORMAL, RoleChannel.CHANNEL_WOLF]
        self._priority = NightPriority.PRIORITY_WOLF
        self._clamp = Clamp.CLAMP_WOLF

    @property
    def clamp(self):
        return self._clamp

    @property
    def priority(self):
        return self._priority.value

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


    async def night_action(self, game, member):
        pass

    async def day_action(self, game, member):
        pass

    async def voting_action(self, game, member):
        pass