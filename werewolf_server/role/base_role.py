from abc import ABC, abstractmethod
from enum import Enum

from werewolf_server.game.base_game import BaseGame
from werewolf_server.model.member import Member


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
    async def night_action(self, game: BaseGame, member: Member):
        pass

    @abstractmethod
    async def day_action(self, game: BaseGame, member: Member):
        pass

    @abstractmethod
    async def voting_action(self, game: BaseGame, member: Member):
        pass


