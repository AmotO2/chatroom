import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=55555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        self.num_clients = 0

    def broadcast(self, message, sender_client):
        for client in self.clients:
            if client != sender_client:
                client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message, client)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast(f'{nickname} left the chat!'.encode('ascii'), client)
                self.num_clients -= 1
                print(f'Ready for next connection. Total connections: {self.num_clients}')
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")

            nickname = client.recv(1024).decode('ascii')
            self.clients.append(client)
            self.nicknames.append(nickname)
            print(f'Nickname of the new connection is {nickname}!')
            self.broadcast(f'{nickname} joined the chat!'.encode('ascii'), client)
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()
            self.num_clients += 1
            print(f'Ready for next connection. Total connections: {self.num_clients}')

    def run(self):
        print("Server is running...")
        self.receive()

if __name__ == "__main__":
    chatserver = ChatServer()
    chatserver.run()