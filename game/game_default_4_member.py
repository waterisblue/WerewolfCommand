import random

from game.base_game import BaseGame
from role.role_civilian import RoleCivilian
from role.role_prophet import RoleProPhet
from role.role_witch import RoleWitch
from role.role_wolf import RoleWolf


class GameDefault4Member(BaseGame):
    def __init__(self):
        self.member = 4
        self.current_member = 0
        self.roles = [RoleProPhet, RoleCivilian, RoleWitch, RoleWolf]


    async def assign_roles(self):
        idx = random.randint(0, len(self.roles) - 1)
        role = self.roles[idx]
        self.roles.remove(role)
        return role

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

if __name__ == '__main__':
    game = GameDefault4Member()
    for i in range(0, 4):
        role = game.assign_roles()
        print(role)