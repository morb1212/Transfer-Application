import RUDP_API
def rudp_socket(destination):
    RUDP_API.rudp_socket(destination)
def rudp_send(data, destination, sock):
    RUDP_API.rudp_send(data, destination, sock)
def rudp_close(sock, destination):
    RUDP_API.close(sock, destination)
def rudp_recv(cur_sock, addr):
    RUDP_API.rudp_recv(cur_sock, addr)


