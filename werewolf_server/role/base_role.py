from abc import ABC, abstractmethod
from enum import Enum


class RoleStatus(Enum):
    STATUS_ALIVE = 0
    STATUS_DEAD = 1
    STATUS_EXILE = 2


class BaseRole(ABC):
    _status: RoleStatus

    @abstractmethod
    async def night_action(self):
        pass

    @abstractmethod
    async def day_action(self):
        pass

    @abstractmethod
    async def voting_action(self):
        pass

    async def get_role_status(self):
        return self._status

    async def set_role_status(self, status: RoleStatus):
        self._status = status
