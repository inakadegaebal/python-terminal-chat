import socket
import threading

IPADDR = "127.0.0.1"
PORT = 49152

sock = socket.socket(socket.AF_INET)
sock.connect((IPADDR, PORT))

def recv_data(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data == b"":
                break
            print(data.decode("utf-8"))
        except ConnectionResetError:
            break

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

thread = threading.Thread(target=recv_data, args=(sock,))
thread.start()

while True:
    data = input("> ")
    if data == "exit":
        break
    else:
        try:
            sock.send(data.encode("utf-8"))
        except ConnectionResetError:
            break

sock.shutdown(socket.SHUT_RDWR)
sock.close()


