import asyncio
import logging

from werewolf_common.model.message import Message

class WerewolfServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.clients = set()

    async def handle_client(self, reader, writer, process_message):
        addr = writer.get_extra_info("peername")
        logging.info(f"New connection from {addr}")
        self.clients.add(writer)

        try:
            while True:
                data = await reader.read(1024)
                await process_message(Message.from_json(data))
                logging.info(f"Received from {addr}: {data}")

        except Exception as e:
            logging.error(f"Error with client {addr}: {e}")
        finally:
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()
            logging.info(f"Connection closed: {addr}")

    async def broadcast(self, message):
        data = message.to_json().encode()
        for client in self.clients:
            try:
                client.write(data)
                await client.drain()
            except Exception as e:
                logging.error(e)
                pass

    async def send_message_by_client(self, message, clients):
        data = message.to_json().encode()
        for client in self.clients:
            try:
                client.write(data)
                await client.drain()
            except Exception as e:
                logging.error(e)
                pass

    async def run(self, process_message):
        server = await asyncio.start_server(
            lambda r, w: self.handle_client(r, w, process_message),
            self.host,
            self.port
        )
        logging.info(f"Server running on {self.host}:{self.port}")

        async with server:
            await server.serve_forever()

