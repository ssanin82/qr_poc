import subprocess
import sys
import time
import socket

server_host, server_port = 'localhost', 50000


class TestClient:
    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((server_host, server_port))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def get_quote(self, security_id, quantity):
        req_bid = '%d BUY %d' % (security_id, quantity)
        req_ask = '%d SELL %d' % (security_id, quantity)
        self.conn.sendall(req_bid.encode())
        bid = float(self.conn.recv(1024).decode())
        self.conn.sendall(req_ask.encode())
        ask = float(self.conn.recv(1024).decode())
        return bid, ask

    def stop_server(self):
        self.conn.sendall('STOP_SERVER'.encode())


if '__main__' == __name__:
    server = subprocess.Popen(['python', 'server.py'], stdout=sys.stdout, stderr=sys.stdout)
    time.sleep(0.1)

    qty = 100
    with TestClient() as c:
        for i in range(100):
            bid, ask = c.get_quote(i, qty)
            print('security: %d, qty: %d, bid: %f, ask: %f' % (i, qty, bid, ask))
        c.stop_server()
    server.wait()
