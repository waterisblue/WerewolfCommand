import asyncio
import logging
import random
from collections import OrderedDict
from typing import List

from fiona.crs import defaultdict

from werewolf_common.model.message import Message
from werewolf_server.game.base_game import BaseGame
from werewolf_server.model.member import Member
from werewolf_server.role.base_role import RoleStatus, Clamp
from werewolf_server.role.role_civilian import RoleCivilian
from werewolf_server.role.role_prophet import RoleProPhet
from werewolf_server.role.role_witch import RoleWitch
from werewolf_server.role.role_wolf import RoleWolf
from werewolf_server.server import WerewolfServer
from werewolf_server.utils.game import circular_access
from werewolf_server.utils.i18n import Language


class GameDefault4Member(BaseGame):
    def __init__(self):
        super().__init__()
        self.max_member = 4
        self.roles = [RoleProPhet, RoleCivilian, RoleWitch, RoleWolf]
        self.day = 1
        self.members: List[Member] = []
        self.speak_time = 10
        self.kill_time = 10
        self.now_killed = None


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
        await WerewolfServer.send_message(
            Message(
                code=Message.CODE_SUCCESS,
                type=Message.TYPE_TEXT,
                detail=Language.get_translation('darkness')
            ),
            *self.members
        )
        members_sorted = sorted(self.members, key=lambda m: m.role.priority)

        members_priority = OrderedDict()

        for member in members_sorted:
            priority = member.role.priority
            if priority not in members_priority:
                members_priority[priority] = []
            members_priority[priority].append(member)
        logging.info(members_priority)
        for _, members in members_priority.items():
            actions = []
            for member in members:
                actions.append(member.role.night_action(game=self, member=member))
            res = await asyncio.gather(*actions)
            # assign dead member
            if members[0].role.clamp == Clamp.CLAMP_WOLF:
                if res:
                    killed_member = res[0]
                    self.now_killed = killed_member
                    killed_member.role.status = RoleStatus.STATUS_DEAD


    async def day_phase(self):
        await WerewolfServer.send_message(
            Message(
                code=Message.CODE_SUCCESS,
                type=Message.TYPE_TEXT,
                detail=Language.get_translation('dawn')
            ),
            *self.members
        )
        start_index = random.randint(0, self.max_member)
        circular_members = circular_access(self.members, start_index)
        alive_members = [m for m in circular_members if m.role.status == RoleStatus.STATUS_ALIVE]
        alive_length = len(alive_members)

        for index, member in enumerate(alive_members):
            if index < alive_length - 1:
                next_member = alive_members[index + 1]
                await WerewolfServer.send_message(
                    Message(
                        code=Message.CODE_SUCCESS,
                        type=Message.TYPE_TEXT,
                        detail=Language.get_translation('speak', no=member.no, next=next_member.no)
                    ),
                    *self.members
                )
            else:
                await WerewolfServer.send_message(
                    Message(
                        code=Message.CODE_SUCCESS,
                        type=Message.TYPE_TEXT,
                        detail=Language.get_translation('speak_last', no=member.no)
                    ),
                    *self.members
                )
            await member.role.day_action(game=self, member=member)
            await WerewolfServer.send_message(
                Message(
                    code=Message.CODE_SUCCESS,
                    type=Message.TYPE_TEXT,
                    detail=Language.get_translation('speak_end', no=member.no)
                ),
                *self.members
            )

    async def voting_phase(self):
        await WerewolfServer.send_message(
            Message(
                code=Message.CODE_SUCCESS,
                type=Message.TYPE_TEXT,
                detail=Language.get_translation('voting')
            ),
            *self.members
        )
        actions = []
        for member in self.members:
            if member.role.status != RoleStatus.STATUS_ALIVE:
                continue
            actions.append(member.role.voting_action(game=self, member=member))
        votes = await asyncio.gather(*actions)

        res = defaultdict(int)
        for vote in votes:
            res[vote] += 1

        vote_res = ''
        for m, v in res.items():
            vote_res += Language.get_translation('exile_member_stat', no=m.no, v=v)

        await WerewolfServer.send_message(
            Message(
                code=Message.CODE_SUCCESS,
                type=Message.TYPE_TEXT,
                detail=Language.get_translation('exile_member_result', res=vote_res)
            ),
            *self.members
        )

        max_votes = max(res.values()) if res else 0

        exiles = [member for member, count in res.items() if count == max_votes]
        if len(exiles) > 1:
            await WerewolfServer.send_message(
                Message(
                    code=Message.CODE_SUCCESS,
                    type=Message.TYPE_TEXT,
                    detail=Language.get_translation('exile_member_equal')
                ),
                *self.members
            )
            return
        exiles = exiles[0]
        exiles.status = RoleStatus.STATUS_EXILE
        await WerewolfServer.send_message(
            Message(
                code=Message.CODE_SUCCESS,
                type=Message.TYPE_TEXT,
                detail=Language.get_translation('exile_member', no=exiles.no)
            ),
            *self.members
        )
        return

    async def check_winner(self):
        wolves_count = sum(1 for member in self.members if member.role.clamp == Clamp.CLAMP_WOLF and member.role.status == RoleStatus.STATUS_ALIVE)
        god_people_count = sum(1 for member in self.members if member.role.clamp == Clamp.CLAMP_GOD_PEOPLE and member.role.status == RoleStatus.STATUS_ALIVE)
        logging.info(f'god people count: {god_people_count}, wolf count: {wolves_count}')
        if wolves_count == 0:
            return Clamp.CLAMP_GOD_PEOPLE
        elif wolves_count >= god_people_count:
            return Clamp.CLAMP_WOLF
        return False

    def add_member(self, member: Member):
        self.members.append(member)

    async def start(self):
        await WerewolfServer.send_message(Message(
            code=Message.CODE_SUCCESS,
            type=Message.TYPE_TEXT,
            detail=Language.get_translation('game_start')
        ), *self.members)
        await WerewolfServer.send_detail(Language.get_translation('game_nos', nos='1, 2, 3, 4'), *self.members)
        for m in self.members:
            await WerewolfServer.send_detail(Language.get_translation('game_no', no=m.no), m)
        await self.assign_roles()
        logging.info('role assigned done.')
        while not await self.check_winner():
            logging.info(f'{self.day} day start.')
            await self.night_phase()
            await self.day_phase()
            await self.voting_phase()

