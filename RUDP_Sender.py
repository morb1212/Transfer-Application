import socket
import time
import RUDP_API


def client_function():
    # Define host and port
    HOST = '127.0.0.1'
    PORT = 12345
    # Create a socket object

    client_socket = RUDP_API.rudp_socket((HOST, PORT))

    with open("test.txt", "wb") as out:
        out.seek((2 * 1024 * 1024) - 1)
        out.write(b'\0')

    FILE_PATH = "test.txt"

    data_to_send = f"{FILE_PATH}"
    print("beginning to send file")
    RUDP_API.rudp_send(data_to_send, (HOST, PORT), client_socket)
    while True:
        # User input loop to control sending the file
        s = input("Do you need the file? Y / N: ")
        if s.upper() == "N":
            RUDP_API.rudp_close(client_socket,(HOST, PORT))
            break
        elif s.upper() == "Y":
            RUDP_API.rudp_send(data_to_send, (HOST, PORT), client_socket)
            print("File transfer completed")
        else:
            print("Unknown input. Please enter 'Y' or 'N'.")


# Run client function directly when this file is executed
if __name__ == "__main__":
    client_function()
