from werewolf_common.model.message import Message
from werewolf_server.game.base_game import BaseGame
from werewolf_server.role.base_role import BaseRole, RoleStatus, RoleChannel, NightPriority, Clamp
from werewolf_server.server import WerewolfServer
from werewolf_server.utils.i18n import Language


class RoleHunter(BaseRole):
    def __init__(self):
        self._status = RoleStatus.STATUS_ALIVE
        self._name = Language.get_translation('hunter')
        self._channels = [RoleChannel.CHANNEL_NORMAL,]
        self._priority = NightPriority.PRIORITY_CIVILIAN
        self._clamp = Clamp.CLAMP_GOD_PEOPLE
        self.bullet = 1

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def name(self):
        return self._name

    @property
    def channels(self):
        return self._channels

    @property
    def priority(self):
        return self._priority

    @property
    def clamp(self):
        return self._clamp

    async def night_action(self, game: BaseGame, member):
        pass

    async def day_action(self, game: BaseGame, member):
        await super().day_action(game, member)

    async def voting_action(self, game: BaseGame, member):
        return await super().voting_action(game, member)

    async def dead_action(self, game, member):
        if self.bullet < 1:
            return
        await WerewolfServer.read_ready(member)
        await WerewolfServer.send_detail(Language.get_translation('hunter_shoot_choose'), member)
        msg = await WerewolfServer.read_message(member)
        action_success = False
        while not action_success:
            if msg.type != Message.TYPE_CHOOSE:
                continue

            if msg.detail == 'k':
                return
            try:
                p_no = msg.detail.split('+')[-1]
                p_no = int(p_no)
            except (ValueError, IndexError):
                await WerewolfServer.send_detail(Language.get_translation('member_no_not_found'), member)
                continue
            for shoot_m in game.members:
                if shoot_m.no == p_no:
                    if shoot_m.role.status != RoleStatus.STATUS_ALIVE:
                        await WerewolfServer.send_detail(Language.get_translation('member_no_not_found'), member)
                        break
                    shoot_m.role.status = RoleStatus.STATUS_DEAD
                    await WerewolfServer.send_detail(Language.get_translation('member_shot', shoot_no=shoot_m.no, no=member.no), *game.members)
                    action_success = True
                    return
            return

    async def last_word_action(self, game, member):
        await super().last_word_action(game, member)
