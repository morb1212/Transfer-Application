import socket

def client_function():
    # Define host and port
    HOST = '127.0.0.1'
    PORT = 12345

    # Define file path to save the received file
    SAVE_PATH = 'received_file.txt'  # Specify the path where you want to save the received file

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT))

    # Receive data from the server
    file_data = b''
    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        file_data += chunk

    # Save the received file data to a file
    with open(SAVE_PATH, 'wb') as file:
        file.write(file_data)

    print("File received and saved.")

    # Close the connection
    client_socket.close()


# Run client function directly when this file is executed
if __name__ == "__main__":
    client_function()
