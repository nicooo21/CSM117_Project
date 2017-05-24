import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('131.179.16.191', 6789))
msg = "Hey!\n"
print("Printing: " + msg)
client_socket.sendall(msg)
while True:
    pass
