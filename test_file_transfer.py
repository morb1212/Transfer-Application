import subprocess
import time
import os
import pkg_resources
from nose.plugins.builtin import module as nose_module

def create_test_file(filename):
    with open(filename, 'wb') as f:
        f.write(b'')

def check_file_received(filename):
    return os.path.exists(filename) and os.path.getsize(filename) > 0

def start_server(server_script):
    script_path = pkg_resources.resource_filename(__name__, server_script)
    return subprocess.Popen(['python3', script_path])

def start_client(client_script, filename, algo):  # Pass the congestion control algorithm to the client function
    script_path = pkg_resources.resource_filename(__name__, client_script)
    return subprocess.Popen(['python3', script_path, filename, algo])  # Pass the algorithm as an argument

test_file = os.path.abspath('test_file.bin')
received_file = os.path.abspath('received_test_file.bin')
create_test_file(test_file)

def teardown_module(test_module):
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(received_file):
        os.remove(received_file)

def test_rudp_file_transfer():
    server_process = start_server('Receiver.py')
    time.sleep(2)  # Give the server some time to start

    client_process = start_client('Sender.py', test_file, 'RENO')  # Specify the congestion control algorithm
    client_process.wait()

    server_process.terminate()
    server_process.wait()

    assert check_file_received(received_file), "RUDP file transfer failed"

def test_tcp_file_transfer():
    server_process = start_server('Receiver.py')
    time.sleep(2)  # Give the server some time to start

    client_process = start_client('Sender.py', test_file, 'CUBIC')  # Specify the congestion control algorithm
    client_process.wait()

    server_process.terminate()
    server_process.wait()

    assert check_file_received(received_file), "TCP file transfer failed"
