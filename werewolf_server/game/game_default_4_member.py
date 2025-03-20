import random

from werewolf_server.game.base_game import BaseGame
from werewolf_server.role.role_civilian import RoleCivilian
from werewolf_server.role.role_prophet import RoleProPhet
from werewolf_server.role.role_witch import RoleWitch
from werewolf_server.role.role_wolf import RoleWolf


class GameDefault4Member(BaseGame):
    def __init__(self):
        self.member = 4
        self.current_member = 0
        self.roles = [RoleProPhet, RoleCivilian, RoleWitch, RoleWolf]
        self.day = 1


    async def assign_roles(self):
        idx = random.randint(0, len(self.roles) - 1)
        rand_role = self.roles[idx]
        self.roles.remove(rand_role)
        return rand_role

    async def night_phase(self):
        pass

    async def day_phase(self):
        pass

    async def voting_phase(self):
        pass

    async def check_winner(self):
        pass

    async def start(self):
        pass
