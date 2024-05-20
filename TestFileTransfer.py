import unittest
import subprocess
import time
import os

class TestFileTransfer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_file = 'test_file.txt'
        cls.received_file = 'received_test_file.txt'
        cls.create_test_file(cls.test_file)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)
        if os.path.exists(cls.received_file):
            os.remove(cls.received_file)

    @classmethod
    def create_test_file(cls, filename):
        with open(filename, 'w') as f:
            f.write('This is a test file for file transfer.')

    def start_server(self, server_script):
        return subprocess.Popen(['python', server_script])

    def start_client(self, client_script, filename):
        return subprocess.Popen(['python', client_script, filename])

    def check_file_received(self, filename):
        return os.path.exists(filename) and os.path.getsize(filename) > 0

    def test_rudp_file_transfer(self):
        server_process = self.start_server('rudp_server.py')
        time.sleep(2)  # Give the server some time to start

        client_process = self.start_client('rudp_client.py', self.test_file)
        client_process.wait()

        server_process.terminate()
        server_process.wait()

        self.assertTrue(self.check_file_received(self.received_file), "RUDP file transfer failed")

    def test_tcp_file_transfer(self):
        server_process = self.start_server('tcp_server.py')
        time.sleep(2)  # Give the server some time to start

        client_process = self.start_client('tcp_client.py', self.test_file)
        client_process.wait()

        server_process.terminate()
        server_process.wait()

        self.assertTrue(self.check_file_received(self.received_file), "TCP file transfer failed")

if __name__ == '__main__':
    unittest.main()
