import socket
import time

def client_function():
    # Define host and port
    HOST = '127.0.0.1'
    PORT = 12345

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT))

    while True:
        # User input loop to control sending the file
        s = input("Do you need the file? Y / N: ")
        print(s)
        if s.upper() == "N":
            break
        elif s.upper() == "Y":
            # Send the file name to the receiver
            FILE_PATH = "received_file.txt"
            client_socket.sendall(FILE_PATH.encode())

            # Open the file and read its contents
            with open(FILE_PATH, 'rb') as file:
                file_data = file.read()

            # Send the file data size to the receiver
            file_data_size = len(file_data)
            client_socket.sendall(str(file_data_size).encode())

            # Send the file data to the receiver
            client_socket.sendall(file_data)

            print("File transfer completed")
        else:
            print("Unknown input. Please enter 'Y' or 'N'.")

    # Close the connection
    client_socket.close()

# Run client function directly when this file is executed
if __name__ == "__main__":
    client_function()
