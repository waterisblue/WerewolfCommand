import asyncio
import logging

from werewolf_common.model.message import Message

logging.basicConfig(level=logging.INFO)

class WerewolfClient:
    def __init__(self, host="127.0.0.1", port=5555):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        logging.info("Connected to server")

        asyncio.create_task(self.listen_for_messages())
        await self.send_messages()

    async def listen_for_messages(self):
        try:
            while True:
                length = await self.reader.read(4)
                length = int.from_bytes(length, byteorder='big')
                data = await self.reader.read(length)
                message = Message.from_json(data)
                logging.info(f"Received: {message}")

        except Exception as e:
            logging.error(f"Error receiving messages: {e}")
        finally:
            logging.info("Disconnected from server")

    async def send_messages(self):
        try:
            while True:
                content = await asyncio.to_thread(input, "Enter message: ")
                if content.lower() == "exit":
                    break

                message = Message(code=0, type="Player", detail=content)
                self.writer.write(message.to_json())
                await self.writer.drain()
        except Exception as e:
            logging.error(f"Error sending messages: {e}")
        finally:
            self.writer.close()
            await self.writer.wait_closed()
            logging.info("Connection closed")


async def main():
    client = WerewolfClient()
    asyncio.create_task(client.connect())
    client1 = WerewolfClient()
    asyncio.create_task(client1.connect())
    client2 = WerewolfClient()
    asyncio.create_task(client2.connect())
    client3 = WerewolfClient()
    asyncio.create_task(client3.connect())
    await asyncio.sleep(100000)

if __name__ == "__main__":
    asyncio.run(main())