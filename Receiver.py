import socket
import time


def set_congestion_control_algorithm(socket_obj, algorithm):
    # Set TCP congestion control algorithm using socket options
    if algorithm == "reno":
        # Set TCP congestion control algorithm to Reno
        socket_obj.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b"reno")
    elif algorithm == "cubic":
        # Set TCP congestion control algorithm to Cubic
        socket_obj.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b"cubic")
    else:
        print("Invalid congestion control algorithm")


def server_function():
    # Define host and port
    HOST = '127.0.0.1'
    PORT = 12345
    fileList = []

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print("Starting Receiver...")
    print("Waiting for TCP connection...")

    client_socket, addr = server_socket.accept()
    print("Sender connected, beginning to receive file...")
    # Set congestion control algorithm

    # Receive congestion control algorithm from the sender
    send = client_socket.recv(1024).decode().split(":")
    algo = send[0]
    print("selecteed algo: "+algo)
    file_name = send[1]
    set_congestion_control_algorithm(server_socket, algo)

    while True:

        if not file_name:
            # If the received data is empty, it means the client has disconnected
            print("Sender sent exit message.")
            break

        print(f"Receiving file: {file_name}")
        start_time = time.time()  # Start time measurement

        # Receive file data from the sender
        with open(file_name, 'rb') as file:
            file_data = file.read()  # Read the content of the file
            file_data_size = len(file_data)

        end_time = time.time()  # End time measurement
        transfer_time = (end_time - start_time) * 1000  # Convert to milliseconds

        # Calculate transfer speed in MB/s
        file_size_mb = file_data_size / (1024 * 1024)  # Convert to megabytes
        transfer_speed = file_size_mb / (transfer_time / 1000)  # Convert transfer time to seconds
        fileList.append((transfer_time, transfer_speed))

        print("File transfer completed")
        print("Waiting for Sender response...")
        file_name = client_socket.recv(1024).decode()
    # Close the client socket
    client_socket.close()

    print("    * Statistics *")
    for i in range(len(fileList)):
        print(f"Run #{i + 1} Data: Time={fileList[i][0]:.2f}ms; Speed={fileList[i][1]:.2f}MB/s")

    # Close the server socket
    server_socket.close()
    print("Receiver end")


# Run server function directly when this file is executed
if __name__ == "__main__":
    server_function()
