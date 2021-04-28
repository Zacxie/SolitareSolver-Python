import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Byg cardArray ud fra openCV output
cardArray = ["AH", "QH", "KH", "10H", "6H", "5S", "3S"]

try:
    client_socket.bind(("localhost", 9999))
except socket.error as err:
    print('bind failed. Error: ' .format(err))
client_socket.listen(10)
print("Connection established")
conn, addr = client_socket.accept()

s = ' '.join([str(elem) for elem in cardArray]) #converts a string array to a string


conn.send(bytes(s+" \r\n", 'UTF-8')) #sends the string to the java server
data = conn.recv(1024) #recieves message from java server

#udskriv det bedst mulige træk i GUI

print("message recieved: " + data.decode(encoding='UTF-8'))
