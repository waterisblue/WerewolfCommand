import asyncio
import logging

from werewolf_server.game.game_default_4_member import GameDefault4Member
from werewolf_server.server import WerewolfServer
from werewolf_server.utils.i18n import Language

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", encoding="utf-8")
    ]
)

GAME_MODE = {
    '1': GameDefault4Member
}

async def main():
    la = Language()
    port = input(la.get_translation('port_need'))

    game_mode = input(la.get_translation('game_mode_select'))
    game = GAME_MODE.get(game_mode)()

    server = WerewolfServer(port=int(port))
    game.set_server(server)
    asyncio.create_task(server.run(game.process_message))

    print(la.get_translation('server_starting', host='0.0.0.0', port=port))
    await asyncio.sleep(10000)




if __name__ == '__main__':
    asyncio.run(main())