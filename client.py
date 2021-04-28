import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cardArray = ["AH", "QH", "KH", "10H", "6H", "5S", "3S"]

try:
    client_socket.bind(("localhost", 9999))
except socket.error as err:
    print('bind failed. Error: ' .format(err))
client_socket.listen(10)
print("Connection established")
conn, addr = client_socket.accept()

i = 0

while True:
    conn.send(bytes("Message to java from python "+str(i)+" \r\n", 'UTF-8'))
    data = conn.recv(1024)
    print("message recieved: " + data.decode(encoding='UTF-8'))
    i = i+1