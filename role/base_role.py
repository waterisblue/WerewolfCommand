from abc import ABC, abstractmethod


class BaseRole(ABC):
    @abstractmethod
    async def night_action(self):
        pass

    @abstractmethod
    async def day_action(self):
        pass

    @abstractmethod
    async def voting_action(self):
        pass
