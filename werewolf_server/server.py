import asyncio
import logging

from werewolf_server.model.message import Message


class WerewolfServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port

    async def handle_client(self, reader, writer, process_message):
        addr = writer.get_extra_info("peername")
        logging.info(f"New connection from {addr}")

        try:
            data = await reader.read(1024)
            if not data:
                return

            message = Message.from_json(data.decode())
            await process_message(message)
        except Exception as e:
            logging.error(f"Error handling client {addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            logging.info(f"Connection closed: {addr}")

    async def run(self, process_message):
        server = await asyncio.start_server(
            lambda r, w: self.handle_client(r, w, process_message),
            self.host,
            self.port,
        )
        addr = server.sockets[0].getsockname()
        logging.info(f"Server running on {addr}")

        async with server:
            await server.serve_forever()

