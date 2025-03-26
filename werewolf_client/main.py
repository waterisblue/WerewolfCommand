import argparse
import asyncio

from werewolf_client.client import WerewolfClient


async def main():
    parser = argparse.ArgumentParser(description="input ip or port")
    parser.add_argument('-i', '--ip', type=str, required=False, help='input ip')
    parser.add_argument('-p', '--port', type=int, required=False, help='input port')
    args = parser.parse_args()

    host = args.ip
    if not host:
        host = input('输入服务器IP：')
    port = args.port
    if not port:
        port = input('输入服务器端口：')
    client = WerewolfClient(host=host, port=int(port))
    print('等待游戏开始...')
    await client.connect()


if __name__ == "__main__":
    asyncio.run(main())