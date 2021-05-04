import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.bind(("localhost", 9999))
except socket.error as err:
    print('bind failed. Error: '.format(err))

client_socket.listen(10)
conn, addr = client_socket.accept()
print("Connection established")



def send(cardArray):
    s = ' '.join([str(elem) for elem in cardArray])  # converts a string array to a string
    conn.send(bytes(s + " \r\n", 'UTF-8'))  # sends the string to the java server


def recieve():
    data = conn.recv()
    print("message recieved: " + data.decode(encoding='UTF-8'))

