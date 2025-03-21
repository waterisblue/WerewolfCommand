import random

from sympy.strategies.core import switch

from werewolf_server.game.base_game import BaseGame
from werewolf_server.role.role_civilian import RoleCivilian
from werewolf_server.role.role_prophet import RoleProPhet
from werewolf_server.role.role_witch import RoleWitch
from werewolf_server.role.role_wolf import RoleWolf


class GameDefault4Member(BaseGame):
    def __init__(self):
        self.__max_member = 4
        self.__roles = [RoleProPhet, RoleCivilian, RoleWitch, RoleWolf]
        self.__day = 1
        self.__members = []
        self.__server = None


    async def assign_roles(self):
        idx = random.randint(0, len(self.__roles) - 1)
        rand_role = self.__roles[idx]
        self.__roles.remove(rand_role)
        return rand_role

    async def night_phase(self):
        pass

    async def day_phase(self):
        pass

    async def voting_phase(self):
        pass

    async def check_winner(self):
        pass

    async def process_message(self, message):
        print(message)

    def set_server(self, server):
        self.__server = server

