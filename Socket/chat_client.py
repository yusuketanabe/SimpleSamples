import socket
import threading


server_address = ('localhost', 6789)
max_size = 4096

def input_msg_loop(sock):
    while True:
        msg = input('>>')
        if msg == ':q':
            break
        elif msg:
            sock.send(msg.encode('utf-8'))

def client_start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    handle_thread = threading.Thread(target=handler,
                                     args=(sock,),
                                     daemon=True)
    handle_thread.start()
    try:
        input_msg_loop(sock)
    finally:
        sock.close()

def handler(sock):
    while True:
        data = sock.recv(1024)
        print("Received: {}".format(data.decode('utf-8')))

if __name__ == '__main__':
    client_start()
