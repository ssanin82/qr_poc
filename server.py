import socket
import logging
import abc
import threading
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(format='%(name)s %(asctime)-15s %(message)s')
server_host, server_port = 'localhost', 50000
MAX_SECURITY_ID = 100
THREAD_POOL_SIZE = 128
log = logging.getLogger('SERVER')
log.setLevel(logging.DEBUG)


class ReferencePriceSourceListener:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def reference_price_changed(self, security_id, price):
        pass  # nothing here, just forces the child class to always implement this method


class PriceStore(ReferencePriceSourceListener):
    def __init__(self):
        self.prices = [100] * MAX_SECURITY_ID
        self.lock = threading.Lock()

    @staticmethod
    def _validate(security_id):
        assert 0 <= security_id < MAX_SECURITY_ID

    def get(self, security_id):
        self._validate(security_id)
        with self.lock:
            return self.prices[security_id]

    def set(self, security_id, price):
        self._validate(security_id)
        with self.lock:
            self.prices[security_id] = price

    def reference_price_changed(self, security_id, price):
        self.set(security_id, price)


class QuoteCalculationEngine:
    @staticmethod
    def calculate_quote_price(sec_id, ref_price, is_buy, qty):
        # XXX meaningless dummy calculation involving all 4 arguments
        return (ref_price + sec_id) + (0.5 if is_buy else -0.5) + float('0.00%d' % qty)


class ReferencePriceSource(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.listeners = list()
        self.do_stop = False

    def subscribe(self, listener):
        self.listeners.append(listener)

    def stop(self):
        self.do_stop = True

    def run(self):
        # XXX dummy price feed
        sec_id, price = 0, 100.
        while not self.do_stop:
            price += 1.
            if 200. >= price:
                price = 100.
            for listener in self.listeners:
                listener.reference_price_changed(sec_id, price)
            sec_id += 1
            sec_id %= MAX_SECURITY_ID


def price_client(server, sock, client_addr):
    log.info('Got connection from %s', client_addr)
    do_stop_server = False
    while True:
        data = sock.recv(1024)
        if not data:
            break
        str_data = data.decode()
        log.debug('Received request: %s' % str_data)
        if 'STOP_SERVER' == str_data:
            do_stop_server = True
            break
        words = str_data.split()
        sec_id, is_buy, qty = int(words[0]), 'BUY' == words[1], int(words[2])
        sock.sendall(str(QuoteCalculationEngine.calculate_quote_price(
            sec_id, server.price_store.get(sec_id), is_buy, qty)).encode())
    log.info('Client %s closed connection', client_addr)
    sock.close()
    if do_stop_server:
        log.info('Stopping server...')
        server.keep_running = False


class StoppablePriceServer:
    def __init__(self, price_store):
        self.price_store = price_store
        self.keep_running = True

    def serve(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        pool = ThreadPoolExecutor(THREAD_POOL_SIZE)
        log.info('Binding to host %s, port %d' % (server_host, server_port))
        sock.bind((server_host, server_port))
        sock.settimeout(0.3)
        sock.listen(5)
        while self.keep_running:
            try:
                client_sock, client_addr = sock.accept()
                log.debug('Client connected from %s', client_addr)
                pool.submit(price_client, self, client_sock, client_addr)
            except socket.timeout:
                pass
        sock.close()


def main():
    price_store = PriceStore()

    log.info('Starting reference price source...')
    price_src = ReferencePriceSource()
    price_src.subscribe(price_store)
    price_src.start()

    log.info('Starting the server...')
    server = StoppablePriceServer(price_store)
    server.serve()

    log.info('Stopping reference price source...')
    price_src.stop()
    price_src.join()
    log.info('Done')


if "__main__" == __name__:
    main()
