import socket

host = "192.168.10.102"
port = 50030

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host, port))
serversock.listen(10)

print('What you name?')
n_msg = input()
if n_msg == '':
    n_msg = 'B'

print("Waiting for connection ...")
clientsock, client_address = serversock.accept()

while True:
    print("Type message ...")
    s_msg = input()
    if s_msg == '':
        break
    print("Sending ...")
    clientsock.sendall((n_msg + ': ' + s_msg).encode('utf-8'))

    rcvmsg = clientsock.recv(1024)
    print(rcvmsg.decode('utf-8'))
    #print("Received -> {}".format(rcvmsg.decode('utf-8')))
    if rcvmsg == '':
        break

clientsock.close()
