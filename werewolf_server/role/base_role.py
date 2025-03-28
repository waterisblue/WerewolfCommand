import asyncio
import logging
from abc import ABC, abstractmethod
from enum import Enum

from werewolf_common.model.message import Message
from werewolf_server.game.base_game import BaseGame
from werewolf_server.server import WerewolfServer
from werewolf_server.utils.i18n import Language
from werewolf_server.utils.time_task import start_timer_task


class RoleStatus(Enum):
    STATUS_ALIVE = 0
    STATUS_DEAD = 1
    STATUS_EXILE = 2

class RoleChannel(Enum):
    CHANNEL_NORMAL = 0
    CHANNEL_WOLF = 1

class NightPriority:
    PRIORITY_CIVILIAN = 0
    PRIORITY_WOLF = 1
    PRIORITY_PROPHET = 10
    PRIORITY_WITCH = 20

class Clamp(Enum):
    CLAMP_GOD_PEOPLE = 0
    CLAMP_WOLF = 1

class BaseRole(ABC):
    @property
    @abstractmethod
    def status(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def channels(self):
        pass

    @property
    @abstractmethod
    def priority(self):
        pass

    @property
    @abstractmethod
    def clamp(self):
        pass

    @abstractmethod
    async def night_action(self, game: BaseGame, member):
        pass

    @abstractmethod
    async def day_action(self, game: BaseGame, member):
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

    @abstractmethod
    async def voting_action(self, game: BaseGame, member):
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
                if msg.type != Message.TYPE_CHOOSE:
                    continue
                if msg.detail == 'k':
                    return
                try:
                    no = int(msg.detail.strip())
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
                await WerewolfServer.send_message(Message(
                    code=Message.CODE_SUCCESS,
                    type=Message.TYPE_TEXT,
                    detail=Language.get_translation('exile_select_no', no=check_member.no)
                ), member)
                exile_success = True
                return check_member
            except Exception as e:
                logging.error(e)

    @abstractmethod
    async def dead_action(self, game, member):
        pass

    @status.setter
    def status(self, value):
        self._status = value


    @abstractmethod
    async def last_word_action(self, game, member):
        speak_done = asyncio.Event()
        speak_done.set()

        def on_timer_done():
            nonlocal speak_done
            speak_done.clear()

        current_seconds = [game.speak_time]
        await start_timer_task(game.speak_time, on_timer_done, current_seconds=current_seconds)
        await WerewolfServer.read_ready(member)
        await WerewolfServer.send_detail(Language.get_translation('last_word_input'), member)
        while speak_done.is_set():
            msg = await WerewolfServer.read_message(member, speak_done)
            if not msg:
                continue
            if msg.type == Message.TYPE_SPARK_DONE:
                break
            await WerewolfServer.send_detail(
                Language.get_translation('speak_show', no=member.no, detail=msg.detail,
                                         seconds=current_seconds[0]),
                *game.members
            )
