import asyncio
import unittest

from werewolf_server.utils import start_timer_task


class TestAsyncTimer(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.results = []

    async def test_async_callback(self):
        async def capture_callback(message):
            self.results.append(message)

        await start_timer_task(1, capture_callback, "异步消息")
        await asyncio.sleep(0.5)
        self.assertNotIn("异步消息", self.results)
        await asyncio.sleep(1.0)
        self.assertIn("异步消息", self.results)

    async def test_normal_callback(self):
        def capture_callback(message):
            self.results.append(message)

        await start_timer_task(1, capture_callback, "普通消息")
        await asyncio.sleep(1.5)
        self.assertIn("普通消息", self.results)

if __name__ == '__main__':
    unittest.main()