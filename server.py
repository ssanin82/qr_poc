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


class QuoteCalculationEngine(ReferencePriceSourceListener, threading.Thread):
    def __init__(self, price_src):
        threading.Thread.__init__(self)
        price_src.subscribe(self)
        self.do_stop = False
        # TODO calculated price storage

    def calculate_quote_price(self, security_id, reference_price, buy, quantity):
        pass  # TODO return from price storage

    def reference_price_changed(self, security_id, price):
        pass  # TODO

    def stop(self):
        self.do_stop = True

    def run(self):
        while not self.do_stop:
            pass  # TODO do something


class ReferencePriceSource(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.listeners = list()
        self.prices = {i: 100 for i in SECURITY_IDS}
        self.do_stop = False

    def subscribe(self, listener):
        self.listeners.append(listener)

    def get(self, security_id):
        assert security_id in SECURITY_IDS
        return self.prices[security_id]

    def stop(self):
        self.do_stop = True

    def run(self):
        # XXX dummy price feed
        sec_id = 0
        while not self.do_stop:
            self.prices[sec_id] = (self.prices[sec_id] + 1) if self.prices[sec_id] < 200 else 100
            for listener in self.listeners:
                listener.reference_price_changed(sec_id, self.prices[sec_id])
            sec_id += 1
            sec_id %= 100


def main():
    log = logging.getLogger('SERVER')
    log.setLevel(logging.DEBUG)

    price_src = ReferencePriceSource()
    price_src.start()

    calc_engine = QuoteCalculationEngine(price_src)
    calc_engine.start()

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

    price_src.stop()
    price_src.join()
    calc_engine.stop()
    calc_engine.join()


if "__main__" == __name__:
    main()
