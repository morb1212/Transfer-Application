import socket

def server_function():
    # Define host and port
    HOST = '127.0.0.1'
    PORT = 12345

    # Define file path
    FILE_PATH = 'path/to/your/file.txt'  # Update this with the path to your file

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print("Server is listening...")

    # Accept a client connection
    client_socket, addr = server_socket.accept()
    print(f"Connected to {addr}")

    # Open the file and read its contents
    with open(FILE_PATH, 'rb') as file:
        file_data = file.read()

    # Send the file data to the client
    client_socket.sendall(file_data)

    # Close the connection
    client_socket.close()
    server_socket.close()

# Run server function directly when this file is executed
if __name__ == "__main__":
    server_function()
