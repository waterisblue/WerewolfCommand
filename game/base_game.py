from abc import ABC, abstractmethod


class BaseGame(ABC):
    @abstractmethod
    async def assign_roles(self):
        pass

    @abstractmethod
    async def night_phase(self):
        pass

    @abstractmethod
    async def day_phase(self):
        pass

    @abstractmethod
    async def voting_phase(self):
        pass

    @abstractmethod
    async def check_winner(self):
        pass