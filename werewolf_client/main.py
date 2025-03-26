import asyncio

from werewolf_client.client import WerewolfClient


async def main():
    host = input('输入服务器IP：')
    port = input('输入服务器端口：')
    client = WerewolfClient(host=host, port=int(port))
    print('等待游戏开始...')
    await client.connect()



if __name__ == "__main__":
    asyncio.run(main())