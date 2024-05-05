import socket
import time
import RUDP_API


def server_function():
    # Define host and port
    HOST = '127.0.0.1'
    PORT = 12345
    fileList = []
    sumSpeed = 0
    sumTime = 0

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set socket options
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind the socket to the host and port
    addr = (HOST, PORT)
    server_socket.bind(addr)

    ack_sent = False
    print("Starting Receiver...")
    print("Waiting for RUDP connection...")

    # Set socket options after binding
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(False)
    try:
        while not ack_sent:
            try:
                bytes_Address_Pair = server_socket.recvfrom(100)  # (data , (ip,port))
                addr = bytes_Address_Pair[1]
                start_msg = b"ack"
                print("Connection request received, sending ACK")
                server_socket.sendto(start_msg, addr)
                msg = server_socket.recvfrom(100)
                if (msg[0]) == b"ackSecond":
                    ack_sent = True
                    print("Sender connected, beginning to receive file...")
            except BlockingIOError:
                continue
    except socket.timeout:
        if not ack_sent:
            print("Timed out waiting for connection request.")
        else:
            print("Timeout occurred while waiting for data.")
    server_socket.setblocking(True)
    server_socket.settimeout(None)
    while True:
        # Receive file data from the sender
        start_time = time.time()  # Start time measurement
        file_msg = RUDP_API.rudp_recv(server_socket, addr)
        end_time = time.time()  # End time measurement
        transfer_time = (end_time - start_time) * 1000  # Convert to milliseconds
        output_file = "received_data.txt"
        if file_msg is None:
            break
        # Open the file using the sanitized filename
        with open(output_file, 'wb') as file:
            file.write(file_msg)
            file_data_size = len(file_msg)
            # Calculate transfer speed in MB/s
            file_size_mb = file_data_size / (1024 * 1024)  # Convert to megabytes
            transfer_speed = file_size_mb / (transfer_time / 1000)  # Convert transfer time to seconds
            fileList.append((transfer_time, transfer_speed))
            sumTime += transfer_time
            sumSpeed += transfer_speed
            print("File transfer completed")
            print("Waiting for Sender response...")

    print("ACK sent")
    print("--------------------")
    print("    * Statistics *")

    for i in range(len(fileList)):
        print(f"Run #{i + 1} Data: Time={fileList[i][0]:.2f}ms; Speed={fileList[i][1]:.2f}MB/s")

    print("Average time=", sumTime / len(fileList), "ms")
    print("Average bandwidth=", sumSpeed / len(fileList), "MB/s")
    # Close the server socket
    server_socket.close()
    print("--------------------")
    print("Receiver end")


# Run server function directly when this file is executed
if __name__ == "__main__":
    server_function()
