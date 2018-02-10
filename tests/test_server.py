import unittest
import subprocess
import sys
import socket
import time
import logging

logging.basicConfig(format='%(name)s %(asctime)-15s %(message)s')
server_host, server_port = 'localhost', 50000


class TestClient:
    def __init__(self):
        self.log = logging.getLogger('CLIENT')
        self.log.setLevel(logging.DEBUG)
        self.conn = None

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((server_host, server_port))

    def close(self):
        self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get(self, security_id, is_buy, quantity):
        req = '%d %s %d' % (security_id, 'BUY' if is_buy else 'SELL', quantity)
        self.log.info('Requesting: ' + req)
        self.conn.sendall(req.encode())
        res = self.conn.recv(1024).decode()
        self.log.info('Received: ' + res)
        return res

    def stop_server(self):
        self.log.info('Stopping the server...')
        self.conn.sendall('STOP'.encode())


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = subprocess.Popen(['python', 'server.py'], stdout=sys.stdout, stderr=sys.stdout)
        time.sleep(0.1)  # XXX can be a better way to make sure the server is already listening for connections

    def tearDown(self):
        with TestClient() as c:
            c.stop_server()
        self.assertEqual(0, self.server.wait())

    def test_simple1(self):
        with TestClient() as c:
            res = c.get(1, True, 3)
            self.assertEqual('1 BUY 3', res)


if '__main__' == __name__:
    unittest.main()

# TODO coverage
