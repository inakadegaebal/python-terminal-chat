import socket
import threading

IPADDR = "127.0.0.1"
PORT = 49152

sock_sv = socket.socket(socket.AF_INET)
sock_sv.bind((IPADDR, PORT))
sock_sv.listen()

client_list = []

def recv_client(sock, addr):
    while True:
        try:
            message = sock.recv(1024) # bufsizeの単位はbytes。2の累乗にすべき。
            if message == b"": # clientがアクセスを切ると0バイトを受信するのでこれで検知ができる。
                break
            
            print("$ say client:{}".format(addr))

            for client in client_list:
                if client[1] != addr: # 自分自身にはsendしない
                    client[0].send(message)
            
        except ConnectionResetError:
            break

    client_list.remove((sock, addr))
    print("- close client:{}".format(addr))

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

while True:
    sock_cl, addr = sock_sv.accept()
    
    client_list.append((sock_cl, addr))
    print("+ join client:{}".format(addr))

    thread = threading.Thread(target=recv_client, args=(sock_cl, addr))
    thread.start()