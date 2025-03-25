import asyncio
import logging

from werewolf_common.model.message import Message
from werewolf_server.game.base_game import BaseGame
from werewolf_server.model.member import Member


class WerewolfServer:
    def __init__(self, game, host='0.0.0.0', port=5555):
        self.game: BaseGame = game
        self.host = host
        self.port = port
        self.count = 0
        self.count_lock = asyncio.Lock()

    async def handle_client(self, reader, writer):
        try:
            addr = writer.get_extra_info("peername")
            async with self.count_lock:
                self.count += 1
                member = Member(self.count, addr, reader, writer)
                self.game.add_member(member)
                if len(self.game.members) == self.game.max_member:
                    logging.info('member enough, game start.')
                    await self.game.start()
            logging.info(f"New connection from {addr}, now member count: {len(self.game.members)}, max count: {self.game.max_member}")
        except Exception as e:
            logging.exception(e)

    @staticmethod
    async def send_message(message, *members):
        data = message.to_json()

        for member in members:
            try:
                logging.info(f'send {data.decode()} to {member.addr}')
                length = len(data)
                member.writer.write(length.to_bytes(4, byteorder='big'))
                member.writer.write(data)
                await member.writer.drain()
            except Exception as e:
                logging.error(e)

    @staticmethod
    async def read_ready(member):
        await member.reader.read(1024)

    @staticmethod
    async def read_message(member):
        length = 0
        while not length:
            length = await member.reader.read(4)
        data = await member.reader.read(length)
        logging.info(f'read {data.decode()} from {member.addr}')
        return Message.from_json(data)

    async def run(self):
        server = await asyncio.start_server(
            lambda r, w: self.handle_client(r, w),
            self.host,
            self.port
        )
        logging.info(f"Server running on {self.host}:{self.port}")

        async with server:
            await server.serve_forever()

