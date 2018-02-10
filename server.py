
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
    pass  # TODO