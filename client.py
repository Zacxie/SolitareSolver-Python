### Gruppe 12 ###
# Christian Kyed - s184210
# Ida Schrader - s195483
# Mads Storgaard-Nielsen - s180076
# Marie Seindal - s185363
# Peter Revsbech - s183760
# Sebastian Bjerre - s163526

import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while 1:
    try:
        print("Trying to establish connection")
        client_socket.bind(("localhost", 9999))

    except socket.error as err:
        time.sleep(2)
        #print('bind failed. Error: '.format(err))
        continue

    client_socket.listen(10)
    conn, addr = client_socket.accept()
    print("Connection established")
    break

def send(cardArray):
    if cardArray == 'END_GAME':
        conn.send(bytes('END_GAME' + "\r\n", 'UTF-8'))  # sends the string to the java server
    if (cardArray == 'EXIT'):
        conn.send(bytes('EXIT' + "\r\n", 'UTF-8'))  # sends the string to the java server
    if cardArray == None or cardArray == 'NONE':
        conn.send(bytes('NONE' + "\r\n", 'UTF-8'))  # sends the string to the java server
    else:
        s = ' '.join([str(elem) for elem in cardArray])  # converts a string array to a string
        conn.send(bytes(s + " \r\n", 'UTF-8'))  # sends the string to the java server


def recieve():
    data = conn.recv(1024)
    msg = data.decode(encoding='UTF-8')
    print(msg)
    return msg


def end_con():
    print("Connection closed")
    conn.close()
    client_socket.close()
