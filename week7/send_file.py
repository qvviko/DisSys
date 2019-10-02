import os
import sys
import socket
from argparse import ArgumentParser


def progress(percent):
    bar_length = 10
    if percent != 100:
        blocks = int(round(bar_length * percent / 100))
        text = f"\rUploading...: [{blocks * '#'}{(bar_length - blocks) * '-'}] {percent:.2f}%"
    else:
        text = f"\rDone!: [{bar_length * '#'}] {percent:.2f}%"
    sys.stdout.write(text)
    sys.stdout.flush()
    pass


def main():
    parser = ArgumentParser(description="Send file")
    parser.add_argument('filename', type=str, help='Name of the file')
    parser.add_argument('hostname', nargs='?', metavar=('hostname',), type=str, default='localhost',
                        help='Name of the server')
    parser.add_argument('port', nargs='?', type=int, metavar=('port',), default=8800, help='Port of the server')

    namespace = parser.parse_args()
    filename = namespace.filename
    port = namespace.port
    hostname = namespace.hostname

    # Connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))

    print(f"Begin transfer of {filename} to {hostname}:{port}")
    f = open(filename, 'rb')
    size = os.path.getsize(filename)
    sock.send(filename.encode())

    ack = sock.recv(1)  # Get ack
    if int(ack.decode()):
        total = 0
        percent = total / size
        # Initialise progress bar
        progress(percent)
        data = f.read(1024)
        # Send data
        while data:
            sock.send(data)
            total += 1024
            percent = total / size
            if percent > 1:
                percent = 1
            progress(percent * 100)
            data = f.read(1024)
    else:
        print("Failed to send filename")
    sock.close()


if __name__ == "__main__":
    main()
