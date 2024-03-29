import socket
import time

ip_address = '192.168.0.10'
port = 7142
packet_interval = 1000
command = 'COMMAND TO SEND'


def connect_to_monitor(ip_address, port):
    """
    Connects to a monitor with the given IP address and port number.

    Parameters:
        ip_address (str): The IP address of the monitor.
        port (int): The port number of the monitor.

    Returns:
        socket.socket: The connected socket object.
    """
    try:
        # Create a new TCP/IP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the monitor
        client_socket.connect((ip_address, port))

        return client_socket

    except socket.error as e:
        print(f"Error connecting to monitor at {ip_address}:{port}: {e}")
        return None


def disconnect_from_monitor(client_socket):
    """
    Disconnects from the monitor by closing the socket.

    Parameters:
        client_socket (socket.socket): The socket object to close.
    """
    # Close the socket
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()


def send_command_to_monitor(client_socket, command, packet_interval):
    """
    Sends the specified command to the monitor at the specified interval and
    returns the response received.

    Parameters:
        client_socket (socket.socket): The connected socket object.
        command (str): The command to send to the monitor.
        packet_interval (int): The interval between packets in milliseconds.

    Returns:
        str: The response received from the monitor.
    """
    # Loop to send commands at the specified interval
    while True:
        # Send a command to the monitor
        client_socket.send(command.encode())

        # Receive a response from the monitor
        response = client_socket.recv(1024)
        response_data = response.decode()
        print('Response received:', response_data)

        # Wait for the specified interval before sending the next command
        time.sleep(packet_interval / 1000)


def receive_message_from_monitor(client_socket):
    """
    Receives a message from the monitor and returns it.

    Parameters:
        client_socket (socket.socket): The connected socket object.

    Returns:
        str: The message received from the monitor.
    """
    # Set the timeout for receiving a message
    client_socket.settimeout(5)

    # Receive the message from the monitor
    try:
        message = client_socket.recv(1024).decode()
        return message

    except socket.timeout:
        print("Timed out waiting for response from monitor")
        return None

    except socket.error as e:
        print(f"Error receiving message from monitor: {e}")
        return None
