import socket

from past.builtins import raw_input

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 5000))
#client_socket.bind(("localhost", 5000))
cardArray = ["AH", "QH", "KH", "10H", "6H", "5S", "3S"]

while True:
    data = raw_input("Starting session")

    if data != 'Q' and data != 'q':
        data = ' '.join([str(elem) for elem in cardArray])
        data = data + "\n"
        client_socket.send(data.encode('utf-8'))
    else:
        data = data + "\n"
        client_socket.send(data.encode('utf-8'))
        client_socket.close()
        break
