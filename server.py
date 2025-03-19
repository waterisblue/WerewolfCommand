import socket
import threading
import json

class WerewolfServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(10)

        print(f"Server started on {host}:{port}")

    def broadcast(self, message, clients):
        for client in clients:
            try:
                client.send(json.dumps(message).encode())
            except:
                self.clients.remove(client)


    def handle_client(self, client):
        data = client.recv(1024).decode()
        if data:
            message = json.loads(data)
            return message

    def run(self):
        while True:
            client, addr = self.server.accept()
            print(f"New connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client,)).start()

