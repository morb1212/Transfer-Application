import socket
import time

def server_function():
    # Define host and port
    HOST = '127.0.0.1'
    PORT = 12346

    # Define file path
    FILE_PATH = 'received_file.txt'  # Update this with the path to your file

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print("Starting Receiver...")
    print("Waiting for TCP connection...")
    # Accept a client connection
    client_socket, addr = server_socket.accept()
    print("Sender connected, beginning to receive file...")
    start_time = time.time()  # Start time measurement

    # Open the file and read its contents
    with open(FILE_PATH, 'rb') as file:
        file_data = file.read()

    # Send the file data to the client
    client_socket.sendall(file_data)

    end_time = time.time()  # End time measurement
    transfer_time = end_time - start_time

    print("File transfer completed")
    print(f"Transfer time: {transfer_time} seconds")

    # Close the connection
    client_socket.close()
    server_socket.close()


# Run server function directly when this file is executed
if __name__ == "__main__":
    server_function()
