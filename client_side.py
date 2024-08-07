import socket
import threading

class ChatClient:
    def __init__(self, host='127.0.0.1', port=55555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        self.nickname = input("Choose a nickname: ")
        self.client.send(self.nickname.encode('ascii'))

        self.write()

    def write(self):
        while True:
            message = input("")
            message_with_nickname = f"{self.nickname}: {message}"
            self.client.send(message_with_nickname.encode('ascii'))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                print(message)
            except:
                print("An error occurred!")
                self.client.close()
                break

if __name__ == "__main__":
    chatclient = ChatClient()
    input("Press Enter to exit...")