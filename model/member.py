class Member:
    STATUS_ONLINE = 0
    STATUS_DISCONNECT = -1
    def __init__(self, name, client):
        self.name = name
        self.client = client
        self.status = Member.STATUS_ONLINE
