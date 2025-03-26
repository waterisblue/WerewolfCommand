import asyncio
import logging

from werewolf_common.model.message import Message
from werewolf_server.role.base_role import BaseRole, RoleStatus, RoleChannel, NightPriority, Clamp
from werewolf_server.server import WerewolfServer
from werewolf_server.utils.i18n import Language
from werewolf_server.utils.time_task import start_timer_task


class RoleProPhet(BaseRole):
    def __init__(self):
        self._status = RoleStatus.STATUS_ALIVE
        self._name = Language.get_translation('prophet')
        self._channels = [RoleChannel.CHANNEL_NORMAL,]
        self._priority = NightPriority.PRIORITY_PROPHET
        self._clamp = Clamp.CLAMP_GOD_PEOPLE

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
        check_success = False
        while not check_success:
            try:
                await WerewolfServer.read_ready(member)
                await WerewolfServer.send_message(Message(
                    code=Message.CODE_SUCCESS,
                    type=Message.TYPE_TEXT,
                    detail=Language.get_translation('check_check_no')
                ), member)
                msg = await WerewolfServer.read_message(member)
                if not msg:
                    continue
                if msg.type != Message.TYPE_CHOOSE:
                    continue
                no = -1
                try:
                    no = int(msg.detail)
                except ValueError:
                    await WerewolfServer.send_detail(Language.get_translation('member_no_not_found'), member)
                    continue
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
                member_role = Language.get_translation('good_man') \
                    if check_member.role.clamp == Clamp.CLAMP_GOD_PEOPLE \
                    else Language.get_translation('wolf')
                await WerewolfServer.send_message(Message(
                    code=Message.CODE_SUCCESS,
                    type=Message.TYPE_TEXT,
                    detail=Language.get_translation('check_member_role', no=check_member.no, role_name=member_role)
                ), member)
                return
            except Exception as e:
                logging.error(e)


    async def day_action(self, game, member):
        await WerewolfServer.send_detail(Language.get_translation('day_speak_now'), member)
        speak_done = asyncio.Event()
        speak_done.set()

        def on_timer_done():
            nonlocal speak_done
            speak_done.clear()
        current_seconds = [game.speak_time]
        await start_timer_task(game.speak_time, on_timer_done, current_seconds=current_seconds)
        await WerewolfServer.read_ready(member)
        while speak_done.is_set():
            msg = await WerewolfServer.read_message(member, speak_done)
            if not msg:
                continue
            if msg.type == Message.TYPE_SPARK_DONE:
                return
            await WerewolfServer.send_detail(
                Language.get_translation('speak_show', no=member.no, detail=msg.detail, seconds=current_seconds[0]),
                *game.members
            )
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