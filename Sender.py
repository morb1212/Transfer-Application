import socket
import time


def client_function():
    # Define host and port
    HOST = '127.0.0.1'
    PORT = 12346

    # Define file path to save the received file
    SAVE_PATH = 'received_file.txt'  # Specify the path where you want to save the received file

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT))
    s = input("do you need the file? Y / N")
    print(s)
    while s!="N":
        if s=="Y":
            start_time = time.time()  # Start time measurement
            # Receive data from the server
            file_data = b''
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                file_data += chunk

            end_time = time.time()  # End time measurement
            transfer_time = end_time - start_time

            print("File transfer completed")
            print(f"Transfer time: {transfer_time} seconds")

            # Save the received file data to a file
            with open(SAVE_PATH, 'wb') as file:
                file.write(file_data)
        else:
            print("unknown")
        s = input("do you need the file? Y / N")
        print(s)


    if s == "N":
        print("didn't send")
        # Close the connection
        client_socket.close()

# Run client function directly when this file is executed
if __name__ == "__main__":
    client_function()