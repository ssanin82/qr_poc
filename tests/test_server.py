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
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((server_host, server_port))
        # XXX no self.conn.close() call

    def get(self, security_id, is_buy, quantity):
        req = '%d %s %d' % (security_id, 'BUY' if is_buy else 'SELL', quantity)
        self.log.info('Requesting: ' + req)
        self.conn.sendall(req.encode())
        data = self.conn.recv(1024)
        print('Received', repr(data))


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = subprocess.Popen(['python', 'server.py'], stdout=sys.stdout, stderr=sys.stdout)
        time.sleep(0.1)  # XXX can be a better way to make sure the server is already listening for connections

    def tearDown(self):
        # TODO send stop signal
        self.server.kill()

    def test_simple1(self):
        c = TestClient()
        c.get(1, True, 3)
        self.assertTrue(True)


if '__main__' == __name__:
    unittest.main()
