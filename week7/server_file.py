import socket
from threading import Thread
import os


class ClientHandler(Thread):
    def __init__(self, sock: socket.socket, server):
        super().__init__(daemon=True)
        self.sock = sock
        self.server = server

    def _close(self):
        self.server.clients.remove(self.sock)
        self.sock.close()

    def run(self):
        orig_filename = self.sock.recv(255).decode()
        self.sock.send('1'.encode())
        ext = orig_filename.split('.')[-1]  # Get extension

        # Get extension (if exists)
        if ext == orig_filename:
            ext = ''
            filename = orig_filename
        else:
            filename = orig_filename[:-len(ext)]

        # Check for copies
        if os.path.exists(orig_filename):
            i = 1
            while os.path.exists(f"{filename}_copy{i}.{ext}"):
                i += 1
            file = open(f'{filename}_copy{i}.{ext}', 'wb')
        else:
            file = open(orig_filename, 'wb')

        print(f"Transfer of {orig_filename} began")
        while True:
            data = self.sock.recv(1024)
            if data:
                file.write(data)
            else:
                print(f"Transfer of {orig_filename} ended")
                self._close()
                return


# Server initialization
class ServerLoader:
    def __init__(self, ip='', port=8800):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen()

        self.clients = []
        print("Server started")

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            print(f"New connection from {addr[0]}")
            self.clients.append(conn)
            ClientHandler(conn, self).start()


def main():
    serv = ServerLoader()
    serv.run()


if __name__ == "__main__":
    main()
