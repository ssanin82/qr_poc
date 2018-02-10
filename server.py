import socket
import logging
import abc
import threading

logging.basicConfig(format='%(name)s %(asctime)-15s %(message)s')
server_host, server_port = 'localhost', 50000
MAX_SECURITY_ID = 100


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
    def calculate_quote_price(security_id, reference_price, buy, quantity):
        pass  # TODO some long running calculation


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
        sec_id, price = 100
        while not self.do_stop:
            price += 1
            if 200 == price:
                price = 100
            for listener in self.listeners:
                listener.reference_price_changed(sec_id, price)
            sec_id += 1
            sec_id %= MAX_SECURITY_ID


def main():
    log = logging.getLogger('SERVER')
    log.setLevel(logging.DEBUG)

    price_store = PriceStore()
    price_src = ReferencePriceSource()

    price_src.subscribe(price_store)
    price_src.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    log.info('Binding to host %s, port %d' % (server_host, server_port))
    s.bind((server_host, server_port))
    s.listen(1)
    conn, addr = s.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        str_data = data.decode()
        log.debug('Received request: %s' % str_data)
        if 'STOP' == str_data:
            log.info('Stopping...')
            break
        words = str_data.split()
        sec_id, is_buy, qty = int(words[0]), 'BUY' == words[1], int(words[2])
        conn.sendall(str(QuoteCalculationEngine.calculate_quote_price(
            sec_id, price_store.get(sec_id), is_buy, qty)).encode())
    conn.close()
    price_src.stop()
    price_src.join()


if "__main__" == __name__:
    main()
