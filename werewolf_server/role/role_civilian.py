import logging
from abc import abstractmethod

from werewolf_common.model.message import Message
from werewolf_server.role.base_role import BaseRole, RoleStatus, RoleChannel, NightPriority, Clamp
from werewolf_server.server import WerewolfServer
from werewolf_server.utils.i18n import Language
from werewolf_server.utils.time_task import start_timer_task


class RoleCivilian(BaseRole):
    def __init__(self):
        self._status = RoleStatus.STATUS_ALIVE
        self._name = Language.get_translation('civilian')
        self._channels =  [RoleChannel.CHANNEL_NORMAL,]
        self._priority = NightPriority.PRIORITY_CIVILIAN
        self._clamp = Clamp.CLAMP_GOD_PEOPLE

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
        speak_done = False

        def on_timer_done():
            nonlocal speak_done
            speak_done = True

        await start_timer_task(game.speak_time, on_timer_done)
        await WerewolfServer.read_ready(member)
        while not speak_done:
            msg = await WerewolfServer.read_message(member)
            if msg.type == Message.TYPE_SPARK_DONE:
                return
            await WerewolfServer.send_message(Message(
                code=Message.CODE_SUCCESS,
                type=Message.TYPE_TEXT,
                detail=f'{member.no}: {msg.detail}'
            ), game.members)
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
                    if m.no == no and m.status == RoleStatus.STATUS_ALIVE:
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