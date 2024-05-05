import socket
import os
import time
import math

CHUNK = 32
LEN_SIZE_DATA = 8
LEN_SIZE_CHUNK = 8
LEN_SIZE_CHECKSUM = 16
LEN_SIZE_ACK = 8
FORMAT = 'utf-8'

def rudp_socket(destination):
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
    CLIENT.setblocking(False)
    CLIENT.settimeout(10)
    print(f'sending start message')
    trying1 = True
    while trying1:
        trying1 = False
        CLIENT.sendto(bytes(CHUNK), destination)
        try:
            temp_pair1 = CLIENT.recvfrom(100)
            if temp_pair1 == b"ack":
                destination = temp_pair1[1]
        except socket.timeout as e:
            trying1 = True
    trying2 = True
    CLIENT.settimeout(3)
    while trying2:
        CLIENT.sendto(b"ackSecond", destination)
        try:
            CLIENT.recvfrom(100)
        except socket.timeout as e:
            trying2 = False
    CLIENT.settimeout(30.0)
    CLIENT.setblocking(True)
    print("RUDP connection established")
    return CLIENT


def checksum(data):
    checksum_value = 0
    for byte in data:
        checksum_value ^= byte
    return checksum_value


def rudp_send(data, destination, sock):
    with open(data, 'rb') as file:
        file_data = file.read()
        chunks = []
        chunk_size = CHUNK
        file_data_size = len(file_data)
        num_chunks = math.ceil(file_data_size / chunk_size)
        for i in range(num_chunks):
            chunk_data = file_data[i * chunk_size:(i + 1) * chunk_size]
            chunk_checksum = checksum(chunk_data)
            size = bytes(f'{file_data_size:<{LEN_SIZE_DATA}}', FORMAT)
            checksum_bytes = bytes(f'{chunk_checksum:<{LEN_SIZE_CHECKSUM}}', FORMAT)
            chunk_index = bytes(f'{i:<{LEN_SIZE_CHUNK}}', FORMAT)
            chunks.insert(i, size + chunk_index + checksum_bytes + chunk_data)
        i = 0
        for chunk in chunks:
            ack_received = False
            while not ack_received:
                try:
                    sock.sendto(chunk, destination)
                    ack_data, _ = sock.recvfrom(LEN_SIZE_ACK)
                    ack = int(ack_data.decode(FORMAT))
                    if ack == i:
                        i += 1
                        ack_received = True
                except socket.timeout:
                    print("Error: Connection timed out while waiting for acknowledgment.")
                    return None
                except ConnectionRefusedError:
                    print("Error: Connection refused.")
                    return None


def rudp_recv(cur_sock, addr):
    get_size = LEN_SIZE_DATA + LEN_SIZE_CHUNK + LEN_SIZE_CHECKSUM + CHUNK
    max_seq_index = 0
    chunks = []
    indexes = []
    bytes_received = 0
    cur_sock.setblocking(True)
    while True:
        msg, _ = cur_sock.recvfrom(get_size)
        if msg == b"close":
            print("Sender sent exit message")
            return None
        if len(msg) >= 25:
            data = msg[LEN_SIZE_DATA + LEN_SIZE_CHUNK: - LEN_SIZE_CHECKSUM]
            calculated = (checksum(data))
            received_checksum = len(msg[-LEN_SIZE_CHECKSUM:])
            if calculated == received_checksum:
                msg_len = int(msg[:LEN_SIZE_DATA])
                index = int(msg[LEN_SIZE_DATA:LEN_SIZE_DATA + LEN_SIZE_CHUNK].decode(FORMAT))
                if index not in indexes:
                    bytes_received += len(data)
                    chunks.insert(0, msg)
                if max_seq_index == index:
                    max_seq_index += 1
                indexes.insert(0, index)
                while max_seq_index in indexes:
                    max_seq_index += 1
                cur_sock.sendto(bytes(f'{index :< {LEN_SIZE_ACK}}', FORMAT), addr)
                if bytes_received >= msg_len:
                    chunks.sort(
                        key=lambda chunk_: int(chunk_[LEN_SIZE_DATA:LEN_SIZE_DATA + LEN_SIZE_CHUNK].decode(FORMAT)))
                    full_msg = b''
                    for ch in chunks:
                        full_msg += ch[LEN_SIZE_DATA + LEN_SIZE_CHUNK: -LEN_SIZE_CHECKSUM]
                    print("ACK sent")
                    return full_msg
def rudp_close(sock, destination):
    try:
        # Send a "close" message to the receiver
        sock.sendto(b"close", destination)
        # Close the socket
        sock.close()
        print("RUDP connection closed successfully.")
    except socket.error as e:
        print(f"Error occurred while closing the RUDP connection: {e}")
