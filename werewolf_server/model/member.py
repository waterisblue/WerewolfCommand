from dataclasses import dataclass

from werewolf_server.role.base_role import BaseRole


@dataclass
class Member:
    STATUS_ONLINE = 0
    STATUS_DISCONNECT = -1

    role: BaseRole

    def __init__(self, no, addr, reader, writer):
        self.no = no
        self.addr = addr
        self.status = Member.STATUS_ONLINE
        self.reader = reader
        self.writer = writer

    def __hash__(self):
        return hash((self.no, self.addr))

    def __eq__(self, other):
        if isinstance(other, Member):
            return self.no == other.no and self.addr == other.addr
        return False

    def __repr__(self):
        return f'Member(no={self.no}, addr={self.addr})'