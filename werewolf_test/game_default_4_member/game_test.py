import unittest

from werewolf_server.game.game_default_4_member import GameDefault4Member
from werewolf_server.role.base_role import BaseRole


class GameTest(unittest.IsolatedAsyncioTestCase):
    async def test_assign_role(self):
        game = GameDefault4Member()
        for i in range(0, 4):
            role = await game.assign_roles()
            self.assertIsInstance(role(), BaseRole)

    async def test_assign_roles_multiple_calls(self):
        roles_assigned = []
        game = GameDefault4Member()
        for _ in range(2):
            roles_assigned.append(await game.assign_roles())
        self.assertEqual(len(set(roles_assigned)), len(roles_assigned))

if __name__ == '__main__':
    unittest.main()