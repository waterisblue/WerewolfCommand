import logging
import random
from typing import List

from werewolf_common.model.message import Message
from werewolf_server.game.base_game import BaseGame
from werewolf_server.model.member import Member
from werewolf_server.role.role_civilian import RoleCivilian
from werewolf_server.role.role_prophet import RoleProPhet
from werewolf_server.role.role_witch import RoleWitch
from werewolf_server.role.role_wolf import RoleWolf
from werewolf_server.server import WerewolfServer
from werewolf_server.utils.i18n import Language


class GameDefault4Member(BaseGame):
    def __init__(self):
        super().__init__()
        self.max_member = 4
        self.roles = [RoleProPhet, RoleCivilian, RoleWitch, RoleWolf]
        self.day = 1
        self.members: List[Member] = []


    async def assign_roles(self):
        for m in self.members[:4]:
            idx = random.randint(0, len(self.roles) - 1)
            rand_role = self.roles[idx]
            self.roles.remove(rand_role)
            m.role = rand_role()
            msg = Message(
                code=Message.CODE_SUCCESS,
                type=Message.TYPE_TEXT,
                detail=Language.get_translation('assign_role', role=m.role.name)
            )
            logging.info(f'{m.addr} assigned role {m.role.name}.')
            await WerewolfServer.send_message(msg, m)


    async def night_phase(self):
        pass

    async def day_phase(self):
        pass

    async def voting_phase(self):
        pass

    async def check_winner(self):
        pass

    def add_member(self, member: Member):
        self.members.append(member)

    async def start(self):
        await WerewolfServer.send_message(Message(
            code=Message.CODE_SUCCESS,
            type=Message.TYPE_TEXT,
            detail=Language.get_translation('game_start')
        ), *self.members)
        await self.assign_roles()
