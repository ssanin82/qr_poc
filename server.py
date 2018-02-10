import socket
import logging

logging.basicConfig(format='%(name)s %(asctime)-15s %(message)s')
server_host, server_port = 'localhost', 50000

class QuoteCalculationEngine:
    def calculate_quote_price(self, security_id, reference_price, buy, quantity):
        pass  # TODO


class ReferencePriceSource:
    def subscribe(self, listener):
        pass  # TODO

    def get(self, security_id):
        pass  # TODO


class ReferencePriceSourceListener:
    def reference_price_changed(self, security_id, price):
        pass  # TODO


if "__main__" == __name__:
    log = logging.getLogger('SERVER')
    log.setLevel(logging.DEBUG)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    log.info('Binding to host %s, port %d' % (server_host, server_port))
    s.bind((server_host, server_port))
    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(1024)
        if not data:
            break
        str_data = data.decode()
        log.debug('Received request: %s' % str_data)
        if 'STOP' == str_data:
            log.info('Stopping...')
            break
        # TODO send response
        conn.sendall(data)
    conn.close()
