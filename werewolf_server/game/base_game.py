from abc import ABC, abstractmethod

class BaseGame(ABC):
    def __init__(self):
        self.last_night_killed = None
        self.kill_time = None
        self.speak_time = None
        self.members = None
        self.max_member = None

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

    @abstractmethod
    def add_member(self, no: int, addr, writer, reader):
        pass

    @abstractmethod
    async def start(self):
        pass