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
    with open("test.txt", "wb") as out:
        out.seek((2 * 1024 * 1024) - 1)
        out.write(b'\0')

    algo = input("select algo RENO or CUBIC: ")
    while algo not in ["reno", "cubic"]:
        algo = input("Invalid algorithm. Choose again: RENO / CUBIC: ")
    client_socket.send(algo.encode())
    FILE_PATH = ":test.txt"
    file="test.txt"
    client_socket.send(FILE_PATH.encode())
    print("File transfer completed")
    while True:
        # User input loop to control sending the file
        s = input("Do you need the file? Y / N: ")
        print(s)
        if s.upper() == "N":
            break
        elif s.upper() == "Y":
            algo = input("select algo RENO or CUBIC: ")
            while algo not in ["reno", "cubic"]:
                algo = input("Invalid algorithm. Choose again: RENO / CUBIC: ")
            client_socket.send(algo.encode())
            # Send the file name to the receiver
            client_socket.send(FILE_PATH.encode())
            print("File transfer completed")
        else:
            print("Unknown input. Please enter 'Y' or 'N'.")

    # Close the connection
    client_socket.close()


# Run client function directly when this file is executed
if __name__ == "__main__":
    client_function()
