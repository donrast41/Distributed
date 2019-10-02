import os
import sys
import socket
from argparse import ArgumentParser


def check_completition(amnt):
    lng = 10
    if amnt != 100:
        blck = int(round(lng * amnt / 100))
        txt = "\rSending (upload): [{}{}] {}%".format(blck * '#',(lng - blck) * '-',amnt)
    else:
        txt = "\rFinished: [{}] {}%".format(lng * '#',amnt)
    sys.stdout.write(txt)
    sys.stdout.flush()
    pass


def main():
    parse_arg = ArgumentParser(description = "Send file")
    parse_arg.add_argument('filename', type = str, help='Name of the file')
    parse_arg.add_argument('hostname', nargs='?', metavar = ('hostname',), type = str, default = 'localhost',
                        help='Name of the server')
    parse_arg.add_argument('port', nargs='?', type=int, metavar=('port',), default=8800, help='Port of the server')

    nm_spc = parse_arg.parse_args()

    filename = nm_spc.filename
    port = nm_spc.port
    hostname = nm_spc.hostname

    #now we connect to server.py
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))

    print("Begin transfer of {} to {}:{}".format(filename,hostname,port))
    f = open(filename, 'rb')
    size = os.path.getsize(filename)
    sock.send(filename.encode())

    acknowledge = sock.recv(1)
    if int(acknowledge.decode()):
        complete = 0
        amnt = complete / size
        # check_completition(amnt)
        file_dt = f.read(1024)
        while file_dt:
            sock.send(file_dt)
            complete += 1024
            amnt = complete / size
            if amnt > 1:
                amnt = 1
            check_completition(amnt * 100)
            file_dt = f.read(1024)
    else:
        print("Failed to send filename")
    sock.close()


if __name__ == "__main__":
    main()
