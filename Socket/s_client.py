import socket


host = "192.168.10.102"
port = 50030

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


print("What you name?")
n_msg = input()
if n_msg == '':
    n_msg = 'A'
#client.send(n_msg.encode('utf-8'))

while True:
    print("Type message ...")
    s_msg = input()
    if s_msg == '':
        break
    print("Sending ...")
    client.sendall((n_msg + ': ' + s_msg).encode('utf-8'))

    response = client.recv(1024)
    print(response.decode('utf-8'))

client.close()
