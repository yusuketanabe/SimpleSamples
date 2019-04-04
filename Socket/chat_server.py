import socket
import threading


server_address = ('localhost', 6789)
max_size = 4096
clients = []

def remove_connection(con, addr):
    print("remove: {}".format(addr))
    con.close()
    clients.remove((con, addr))

def server_start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(server_address)
    server.listen(10)

    while True:
        con, addr = server.accept()
        print("connect: {}".format(addr))
        clients.append((con, addr))
        handle_thread = threading.Thread(target=handler,
                                         args=(con, addr),
                                         daemon=True)
        handle_thread.start()

def handler(con, addr):
    while True:
        try:
            data = con.recv(1024)
        except ConnectionResetError:
            remove_connection(con, addr)
            break
        else:
            if not data:
                remove_connection(con, addr)
                break
            else:
                print("Received: {}".format(addr, data.decode('utf-8')))
                for c in clients:
                    c[0].sendto(data, c[1])

if __name__ == '__main__':
    server_start()
