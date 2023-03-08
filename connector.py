import socket

# Set the IP address and port number
ip_address = '192.168.0.10'
port = 7142

# Create a new TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the monitor
client_socket.connect((ip_address, port))

# Send a command to the monitor
command = 'COMMAND TO SEND'
client_socket.send(command.encode())

# Receive a response from the monitor
response = client_socket.recv(8)
response_data = response.decode()
print('Response received:', response_data)

# Close the socket
client_socket.shutdown(socket.SHUT_RDWR)
client_socket.close()