import socket
import time


def set_congestion_control_algorithm(socket_obj, algorithm):
    print("received with: "+algorithm+ ", choose the algo for the bonus")
    algo = input("select algo RENO or CUBIC: ")
    while algo not in ["reno", "cubic"]:
        algo = input("Invalid algorithm. Choose again: RENO / CUBIC: ")
    # Set TCP congestion control algorithm using socket options
    if algo == "cubic":
        # Set TCP congestion control algorithm to Reno
        socket_obj.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b"cubic")
    elif algo == "reno":
        # Set TCP congestion control algorithm to Cubic
        socket_obj.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b"reno")
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
    algo = -1

    while True:
        # Receive congestion control algorithm from the sender
        data = client_socket.recv(1024).decode()
        if not data:
            break
        send = data.split(":")
        if len(send) < 2:
            print("Invalid data format received.")
            break
        algo = send[0]
        file_name = send[1]
        set_congestion_control_algorithm(server_socket, algo)
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
        if not algo:
            break

    print("Sender sent exit message.")
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
