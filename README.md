# File Transfer Application

This application enables the transfer of files between a client and a server using Reliable UDP (RUDP) and Transmission Control Protocol (TCP).

## RUDP File Transfer

### `RUDP_API.py`

This module contains functions for establishing a reliable UDP connection, sending data, receiving data, and closing the connection.

- `rudp_socket(destination)`: Establishes a reliable UDP socket connection.
- `rudp_send(data, destination, sock)`: Sends data over the RUDP connection.
- `rudp_recv(cur_sock, addr)`: Receives data over the RUDP connection.
- `rudp_close(sock, destination)`: Closes the RUDP connection.

### `rudp_server.py`

This script implements the server side of the RUDP file transfer application.

- `server_function()`: Starts the RUDP server and handles file reception from the client.

### `rudp_client.py`

This script implements the client side of the RUDP file transfer application.

- `client_function()`: Starts the RUDP client and handles file transmission to the server.

## TCP File Transfer

### `tcp_server.py`

This script implements the server side of the TCP file transfer application.

- `server_function()`: Starts the TCP server and handles file reception from the client.

### `tcp_client.py`

This script implements the client side of the TCP file transfer application.

- `client_function()`: Starts the TCP client and handles file transmission to the server.

## Congestion Control

Both the TCP server and client scripts include functionality to select a congestion control algorithm.

- `set_congestion_control_algorithm(socket_obj, algorithm)`: Sets the congestion control algorithm for a TCP socket.

## Usage
run server and then client

1. Start the appropriate server script (`RUDP_Receiver.py` or `Receiver.py`).
2. Start the corresponding client script (`RUDP_Sender.py` or `Sender.py`).
3. Follow the on-screen instructions to initiate file transfer and select congestion control algorithms.

## Note

Ensure that both the client and server are running on the same network and have network connectivity.
## Test

RUN TestFileTransfer.py
Expected result: received_test_file and no error messages upon test complition
