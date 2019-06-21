from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from os import system
from pathlib import Path
from time import sleep

encoding = "utf-8"
buff = 2048

HERE = Path(__file__).parent
CONN_ERRORS = (ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError, ConnectionError)


def connect():
    global sock
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(("127.0.0.1", 5784))


while True:
    try:
        connect()
        break
    except CONN_ERROS:
        continue

while True:
    msg = input(">> ")
    if msg.lower() == "cls":
        system("cls")
        continue
    if msg.lower() == "connect":
        sock.send("dc".encode(encoding))
        connect()
        continue
    if msg.lower() == "exit":
        sock.send("logout".encode(encoding))
        sock.send(msg.lower().encode(encoding))
        exit(-1)
    if msg.lower().startswith("upload"):
        try:
            sock.send(msg.encode(encoding))
            sleep(1)
            parts = msg.split(" ")
            if len(parts) != 5:
                continue
            file = parts[parts.index("file") + 1]
            mode = parts[-1]
            if file == "manually":
                continue
            path = (HERE / "Files" / file).resolve()
            if mode == "binary":
                kwargs = {"mode": "rb"}
                binary = True
            else:
                kwargs = {"encoding": encoding}
                binary = False
            with open(str(path), **kwargs) as file:
                block = file.read(buff)
                while block:
                    if binary:
                        sock.send(bytes(block))
                    else:
                        sock.send(block.encode(encoding))
                    block = file.read(buff)
                if binary:
                    sock.send(b"\x04")
                else:
                    sock.send("\u0004".encode(encoding))
                print("File was sent successfully!")
                continue
        except FileNotFoundError as e:
            print(e)
            continue
    if msg == "<S>EOF<S>":
        msg = "\u0004"
    try:
        sock.send(msg.encode(encoding))
    except CONN_ERRORS:
        try:
            sock.connect(("127.0.0.1", 5784))
            sock.send(msg.encode(encoding))
            continue
        except OSError:
            del sock
            connect()
            sock.send(msg.encode(encoding))
        except CONN_ERRORS:
            continue
