from werewolf_common.model.message import Message
from werewolf_server.role.base_role import BaseRole, RoleStatus, RoleChannel, NightPriority, Clamp
from werewolf_server.role.role_hunter import RoleHunter
from werewolf_server.server import WerewolfServer
from werewolf_server.utils.i18n import Language


class RoleWitch(BaseRole):
    def __init__(self):
        self._status = RoleStatus.STATUS_ALIVE
        self._name = Language.get_translation('witch')
        self._channels = [RoleChannel.CHANNEL_NORMAL,]
        self._priority = NightPriority.PRIORITY_WITCH
        self._clamp = Clamp.CLAMP_GOD_PEOPLE
        self.antidote = 1
        self.poison = 1

    @property
    def clamp(self):
        return self._clamp

    @property
    def priority(self):
        return self._priority

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
        dead_member = None
        if game.last_night_killed:
            dead_member = list(game.last_night_killed)[0]
        if dead_member:
            await WerewolfServer.send_message(Message(
                code=Message.CODE_SUCCESS,
                type=Message.TYPE_TEXT,
                detail=Language.get_translation('night_dead', no=dead_member.no)
            ), member)
        else:
            await WerewolfServer.send_message(Message(
                code=Message.CODE_SUCCESS,
                type=Message.TYPE_TEXT,
                detail=Language.get_translation('night_no_dead')
            ), member)
        action_success = False
        while not action_success:
            await WerewolfServer.read_ready(member)
            await WerewolfServer.send_message(Message(
                code=Message.CODE_SUCCESS,
                type=Message.TYPE_TEXT,
                detail=Language.get_translation('save_or_poison')
            ), member)
            msg = await WerewolfServer.read_message(member)

            if msg.type == Message.TYPE_CHOOSE:
                if msg.detail == 's' and self.antidote > 0:
                    if len(game.last_night_killed) < 1:
                        continue
                    self.antidote -= 1
                    game.last_night_killed.clear()
                    action_success = True
                    return
                if msg.detail.startswith('p') and self.poison > 0:
                    p_no = -1
                    try:
                        p_no = msg.detail.split('+')[-1]
                        p_no = int(p_no)
                    except (ValueError, IndexError):
                        await WerewolfServer.send_detail(Language.get_translation('member_no_not_found'), member)
                        continue
                    for poison_m in game.members:
                        if poison_m.no == p_no:
                            if poison_m.role.status != RoleStatus.STATUS_ALIVE:
                                await WerewolfServer.send_detail(Language.get_translation('member_no_not_found'),member)
                                break
                            # hunter bullet
                            if isinstance(poison_m, RoleHunter):
                                poison_m.bullet = 0
                            game.last_night_killed.add(poison_m)
                    self.poison -= 1
                    action_success = True
                    return
                if msg.detail == 'k':
                    action_success = True
                    return

    async def day_action(self, game, member):
        await super().day_action(game, member)

    async def voting_action(self, game, member):
        return await super().voting_action(game, member)

    async def dead_action(self, game, member):
        pass

    async def last_word_action(self, game, member):
        await super().last_word_action(game, member)