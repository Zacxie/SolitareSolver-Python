import socket

from past.builtins import raw_input

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect(("localhost", 5000))
#client_socket.bind(("localhost", 5000))
cardArray = ["AH", "QH", "KH", "10H", "6H", "5S", "3S"]

try:
    client_socket.bind(("localhost",9999))
except socket.error as err:
    print('bind failed. Error: ' .format(err))
client_socket.listen(10)
print("socket listening")
conn, addr = client_socket.accept()

i =0

while(True):
    conn.send(bytes("Message "+str(i)+" \r\n",'UTF-8'))
    print("Message sent "+ str(i))
    data = conn.recv(1024)
    print(data.decode(encoding='UTF-8'))
    i=i+1

# while True:
#     data = raw_input("Starting session")
#
#     if data != 'Q' and data != 'q':
#         data = ' '.join([str(elem) for elem in cardArray])
#         data = data + "\n"
#         client_socket.send(data.encode('utf-8'))
#     else:
#         data = data + "\n"
#         client_socket.send(data.encode('utf-8'))
#         client_socket.close()
#         break
