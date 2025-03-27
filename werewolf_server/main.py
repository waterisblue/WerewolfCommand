import asyncio
import logging

from werewolf_server.game.game_default_4_member import GameDefault4Member
from werewolf_server.game.game_default_8_member import GameDefault8Member
from werewolf_server.server import WerewolfServer
from werewolf_server.utils.i18n import Language
import argparse

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", encoding="utf-8")
    ]
)

GAME_MODE = {
    '1': GameDefault4Member,
    '2': GameDefault8Member
}

async def main():
    parser = argparse.ArgumentParser(description="input ip or game mode")
    parser.add_argument('-p', '--port', type=int, required=False, help='input port')
    parser.add_argument('-m', '--mode', type=str, required=False, help='input game mode')
    args = parser.parse_args()

    port = args.port
    if not port:
        port = input(Language.get_translation('port_need'))

    game_mode = args.mode
    if not game_mode:
        game_mode = input(Language.get_translation('game_mode_select'))
    # port = 5555
    # game_mode = '1'
    game = GAME_MODE.get(game_mode)()
    server = WerewolfServer(game=game, port=int(port))
    game.server = server
    print(Language.get_translation('server_starting', host='0.0.0.0', port=port))
    await server.run()





if __name__ == '__main__':
    asyncio.run(main())