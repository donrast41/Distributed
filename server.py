import socket
from threading import Thread
import os

class TransferToClient(Thread):
    def __init__(self, sock: socket.socket, server):
        super().__init__(daemon=True)
        self.sock = sock
        self.server = server

    def _close(self):
        self.server.clients.remove(self.sock)
        self.sock.close()

    def run(self):
        name_of_file = self.sock.recv(255).decode()
        self.sock.send('1'.encode())
        #here we are getting the extension of the file (.pdf or any)
        extension = name_of_file.split('.')[-1]
        # Now we are checking if it exists or not
        if extension == name_of_file:
            extension = ''
            nameFile = name_of_file
        else:
            nameFile = name_of_file[:-len(extension)]
        #Duplication examination
        if os.path.exists(name_of_file):
            x = 1
            while os.path.exists(f"{nameFile}_copy{x}.{extension}"):
                x += 1
            f = open(f'{nameFile}_copy{x}.{extension}', 'wb')
        else:
            f = open(name_of_file, 'wb')

        print(f"{name_of_file} is now being transferred")

        while True:
            file_dt = self.sock.recv(1024)
            if file_dt:
                f.write(file_dt)
            else:
                print(f"{name_of_file} is successfully transferred")
                self._close()
                return

class Initalization_Of_Server:
    def __init__(self, ip = '', port = 8800):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen()

        self.clients = []
        print("Initalization_Of_Server Successfull")

    def run(self):
        while True:
            connection, address = self.sock.accept()
            print(f"{address[0]} gives the new connection")
            self.clients.append(connection)
            TransferToClient(connection, self).start()


def main():
    server = Initalization_Of_Server()
    server.run()


if __name__ == "__main__":
    main()
