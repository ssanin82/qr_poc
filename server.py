import socket
import logging
import abc
import threading

logging.basicConfig(format='%(name)s %(asctime)-15s %(message)s')
server_host, server_port = 'localhost', 50000
SECURITY_IDS = range(100)


class ReferencePriceSourceListener:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def reference_price_changed(self, security_id, price):
        pass  # nothing here, just forces the child class to always implement this method


# TODO calculated price storage
class QuoteCalculationEngine(ReferencePriceSourceListener):
    # TODO this should be updated each time there is an updatre on reference price
    def calculate_quote_price(self, security_id, reference_price, buy, quantity):
        pass  # TODO

    def start(self, price_src):
        price_src.subscribe(self)

    def reference_price_changed(self, security_id, price):
        pass


class ReferencePriceSource(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.listeners = list()
        self.prices = {i: 100 for i in SECURITY_IDS}

    def subscribe(self, listener):
        self.listeners.append(listener)

    def get(self, security_id):
        assert security_id in SECURITY_IDS
        return self.prices[security_id]

    def run(self):
        pass  # TODO


if "__main__" == __name__:
    log = logging.getLogger('SERVER')
    log.setLevel(logging.DEBUG)

    price_src = ReferencePriceSource()
    price_src.start()

    calc_engine = QuoteCalculationEngine()
    calc_engine.start(price_src)

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
