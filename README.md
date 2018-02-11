# Quote Server

Due to time available, python was chosen as the language of implementation. Being the most efficient to me for implementing various POCs, despite it's drawbacks, it still allows me to demonstrate basic architectural understanding, multithreading, TDD and some other crucial concepts.

Python 3.6 was chosen for the implementation. I tried not to use any advanced Python modules, only standard ones. If it is necessary ot run it on Python 2.6.6 that goes with basic RedHat Linux installation, only minimamal (if any) changes should be made. Though, I haven't tested it with Python 2.6.6.

## Requirements Summary

* Requests should be handled via TCP connection.
* There can be more than one client.
* Maximize throughput and minimize response time (assume quoted price calculation takes long time to complete).
* Request format: `{security ID} (BUY|SELL) {quantity}` (security id and quantity are integers).
* Response format: a single line with a numeric value representing the quoted price.
* Suggested interfaces:
  - `QuoteCalculationEngine::calculate_quote_price(sec_id, ref_price, buy, qty)`
  - `ReferencePriceSource::subscribe(listener)`
  - `ReferencePriceSource::get(sec_id)`
  - `ReferencePriceSourceListener::reference_price_changed(sec_id, price)`

## Architectural Decisions

### Assumptions and Simplifications

* There shall be 100 securities with their ids ranging from 0 to 99. Initial price for all the securities is 100.
* Even though Python has problems with native threading (because of the GIL mechanism - watch first 4 minutes of [this](https://www.youtube.com/watch?v=Obt-vMVdM8s) video), for simplicity we'll use Python threads anyway. Similar architectural decisions in Java or C++ would not have this issue. We just assume there is no GIL in Python (the drawback is that if we try doing performance tests on this, the result will be inconsistent with what we would expect from C++/Java - other performance optimization techniques are required for Python - for, example, multiprocessing).
* Dummy price feed: shall be simplified to a separate thread going through each security one by one and incrementing its price.
* Dummy price calculation: one-liner in the code that has little meaning. The only requirements I set to the formula is to have it depending on all 4 arguments and bid should be lower than ask.
* Assuming that the request passed is always correct (that is security id and quantity are always numeric, side is always BUY or SELL). Validation is omitted.
* Price storage (refer to implementation details for the reason there is a separate price storage) is just an array protected by a mutex. For the given particular case of security id range between 0 and 99 having an array is more efficient than using a map to store the price (considering no security ids will be added or removed, only values in the storage will be changed).

### Implementation Details





---
* There shall be price storage............
* We can't pre-calculate the requested price in a separate thread and return the value on request because the calculation depends on quantity which is known only at the time of the request. Hence, a way to speed up response time and
* TODO describe interface changes (no get in ReferencePriceSource)

### Running the App

TODO

### TODO

* Grammarly
