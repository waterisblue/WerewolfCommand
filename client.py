import socket
import json
import threading

class WerewolfClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.username = input("Enter your name: ")
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()
        self.send_message({'type': 'join', 'name': self.username})

    def send_message(self, message):
        try:
            self.client.send(json.dumps(message).encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                if data:
                    message = json.loads(data)
                    self.handle_message(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def handle_message(self, message):
        if message['type'] == 'update':
            print(f"Server update: {message['message']}")
        elif message['type'] == 'vote':
            # Handle vote-related updates here
            pass

    def vote(self, target):
        self.send_message({'type': 'vote', 'target': target})

    def close(self):
        self.client.close()

# Usage
if __name__ == "__main__":
    client = WerewolfClient()
    while True:
        action = input("Enter action (vote <name> / quit): ")
        if action.startswith('vote'):
            target = action.split(' ')[1]
            client.vote(target)
        elif action == 'quit':
            client.close()
            break
