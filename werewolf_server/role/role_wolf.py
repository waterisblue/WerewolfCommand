from werewolf_server.role.base_role import BaseRole


class RoleWolf(BaseRole):
    async def night_action(self):
        pass

    async def day_action(self):
        pass

    async def voting_action(self):
        pass