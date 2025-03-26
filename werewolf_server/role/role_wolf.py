import asyncio
import logging

from werewolf_common.model.message import Message
from werewolf_server.role.base_role import BaseRole, RoleStatus, RoleChannel, NightPriority, Clamp
from werewolf_server.server import WerewolfServer
from werewolf_server.utils.i18n import Language
from werewolf_server.utils.time_task import start_timer_task


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
        speak_done = asyncio.Event()
        speak_done.set()
        def on_timer_done():
            nonlocal speak_done
            speak_done.clear()
        wolf_members = [m for m in game.members if m.role.clamp == Clamp.CLAMP_WOLF]
        wolf_no = ','.join([str(m.no) for m in wolf_members])
        await WerewolfServer.send_message(Message(
            code=Message.CODE_SUCCESS,
            type=Message.TYPE_TEXT,
            detail=Language.get_translation('wolf_action', time=game.kill_time, wolfs=wolf_no)
        ), member)

        await WerewolfServer.read_ready(member)

        wolf_members = [m for m in game.members if RoleChannel.CHANNEL_WOLF in m.role.channels]
        check_member = None
        await start_timer_task(game.kill_time, on_timer_done)
        while speak_done.is_set():
            logging.info('wolf choose kill member')
            msg = await WerewolfServer.read_message(member, speak_done)
            if not msg:
                continue
            if msg.type == Message.TYPE_CHOOSE:
                no = -1
                try:
                    no = int(msg.detail)
                except ValueError:
                    await WerewolfServer.send_detail(Language.get_translation('member_no_not_found'), member)
                    continue
                for m in game.members:
                    if m.no == no and m.role.status == RoleStatus.STATUS_ALIVE:
                        check_member = m
                if not check_member:
                    await WerewolfServer.send_message(Message(
                        code=Message.CODE_SUCCESS,
                        type=Message.TYPE_TEXT,
                        detail=Language.get_translation('member_no_not_found')
                    ), member)
                else:
                    await WerewolfServer.send_message(Message(
                        code=Message.CODE_SUCCESS,
                        type=Message.TYPE_TEXT,
                        detail=Language.get_translation('kill_member', no=check_member.no)
                    ), member)
                continue
            await WerewolfServer.send_message(Message(
                code=Message.CODE_SUCCESS,
                type=Message.TYPE_TEXT,
                detail=f'{member.no}: {msg.detail}'
            ), *wolf_members)
        return check_member

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