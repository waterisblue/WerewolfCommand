from abc import ABC, abstractmethod
from enum import Enum


class RoleStatus(Enum):
    STATUS_ALIVE = 0
    STATUS_DEAD = 1
    STATUS_EXILE = 2

class RoleChannel(Enum):
    CHANNEL_NORMAL = 0
    CHANNEL_WOLF = 1

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

    @abstractmethod
    async def night_action(self, member):
        pass

    @abstractmethod
    async def day_action(self, member):
        pass

    @abstractmethod
    async def voting_action(self, member):
        pass


