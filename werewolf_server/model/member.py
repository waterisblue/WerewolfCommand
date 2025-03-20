from dataclasses import dataclass

from werewolf_client.client import WerewolfClient
from werewolf_server.role.base_role import BaseRole


@dataclass
class Member:
    STATUS_ONLINE = 0
    STATUS_DISCONNECT = -1

    name: str
    role: BaseRole
    client: WerewolfClient
    def __init__(self, name, client):
        self.name = name
        self.client = client
        self.status = Member.STATUS_ONLINE
