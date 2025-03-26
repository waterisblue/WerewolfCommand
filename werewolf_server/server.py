import asyncio
import logging

from werewolf_common.model.message import Message
from werewolf_server.game.base_game import BaseGame


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
                self.game.add_member(self.count, addr, writer, reader)
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
    async def send_detail(detail, *members):
        data = Message(
            code=Message.CODE_SUCCESS,
            type=Message.TYPE_TEXT,
            detail=detail
        ).to_json()
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
        try:
            while True:
                data = await asyncio.wait_for(member.reader.read(1024), timeout=0.1)
                if not data:
                    break
        except asyncio.TimeoutError:
            pass

    @staticmethod
    async def read_message(member, speak_done=None):
        length = 0
        length_data = b''
        while length < 4:
            if speak_done and not speak_done.is_set():
                return None
            try:
                chunk = await asyncio.wait_for(member.reader.read(4 - length), timeout=0.1)
                length += len(chunk)
                length_data += chunk
            except asyncio.TimeoutError:
                continue
        data = await member.reader.read(int.from_bytes(length_data, byteorder='big'))
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
