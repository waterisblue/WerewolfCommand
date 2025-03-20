import socket
import threading
import json
import logging

class WerewolfServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(10)

        logging.info(f"Server started on {host}:{port}")


    def handle_client(self, client):
        data = client.recv(1024).decode()
        if data:
            message = json.loads(data)
            return message

    def run(self):
        while True:
            client, addr = self.server.accept()
            logging.info(f"New connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client,)).start()

