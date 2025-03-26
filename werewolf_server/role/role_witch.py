import asyncio
import logging


from werewolf_common.model.message import Message
from werewolf_server.role.base_role import BaseRole, RoleStatus, RoleChannel, NightPriority, Clamp
from werewolf_server.server import WerewolfServer
from werewolf_server.utils.i18n import Language
from werewolf_server.utils.time_task import start_timer_task


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
                            game.last_night_killed.add(poison_m)
                    self.poison -= 1
                    action_success = True
                    return
                if msg.detail == 'k':
                    action_success = True
                    return

    async def day_action(self, game, member):
        await WerewolfServer.send_detail(Language.get_translation('day_speak_now'), member)
        speak_done = asyncio.Event()
        speak_done.set()

        def on_timer_done():
            nonlocal speak_done
            speak_done.clear()

        await start_timer_task(game.speak_time, on_timer_done)
        await WerewolfServer.read_ready(member)
        while speak_done.is_set():
            msg = await WerewolfServer.read_message(member, speak_done)
            if not msg:
                continue
            if msg.type == Message.TYPE_SPARK_DONE:
                return
            await WerewolfServer.send_message(Message(
                code=Message.CODE_SUCCESS,
                type=Message.TYPE_TEXT,
                detail=f'{member.no}: {msg.detail}'
            ), *game.members)
        return

    async def voting_action(self, game, member):
        exile_success = False
        while not exile_success:
            try:
                await WerewolfServer.read_ready(member)
                await WerewolfServer.send_message(Message(
                    code=Message.CODE_SUCCESS,
                    type=Message.TYPE_TEXT,
                    detail=Language.get_translation('exile_input_no')
                ), member)
                msg = await WerewolfServer.read_message(member)
                no = int(msg.detail.strip())
                check_member = None
                for m in game.members:
                    if m.no == no and m.role.status == RoleStatus.STATUS_ALIVE:
                        check_member = m
                if not check_member:
                    await WerewolfServer.send_message(Message(
                        code=Message.CODE_SUCCESS,
                        type=Message.TYPE_TEXT,
                        detail=Language.get_translation('member_no_not_found')
                    ), member)
                    continue
                await WerewolfServer.send_message(Message(
                    code=Message.CODE_SUCCESS,
                    type=Message.TYPE_TEXT,
                    detail=Language.get_translation('exile_select_no', no=check_member.no)
                ), member)
                exile_success = True
                return check_member
            except Exception as e:
                logging.error(e)