# Quote Server

Due to time available, python was chosen as the language of implementation. Being the most efficient to me for implementing various POCs, despite it's drawbacks, it still allows me to demonstrate basic architectural understanding, multithreading, TDD and some other crucial concepts.

Python 3.6 was chosen for the implementation. I tried not to use any advanced Python modules, only standard ones. If it is necessary to run it on Python 2.6.6 that goes with basic RedHat Linux installation, only minimal (if any) changes should be made. Though, I haven't tested it with Python 2.6.6.

## Requirements Summary

* Requests should be handled via TCP connection.
* There can be more than one client.
* Maximize throughput and minimize response time (assume quoted price calculation takes a long time to complete).
* Request format: `{security ID} (BUY|SELL) {quantity}` (security id and quantity are integers).
* Response format: a single line with a numeric value representing the quoted price.
* Suggested interfaces:
  - `QuoteCalculationEngine::calculate_quote_price(sec_id, ref_price, buy, qty)`
  - `ReferencePriceSource::subscribe(listener)`
  - `ReferencePriceSource::get(sec_id)`
  - `ReferencePriceSourceListener::reference_price_changed(sec_id, price)`

## Architectural Decisions

### Assumptions and Simplifications

* There shall be 100 securities with their ids ranging from 0 to 99. The initial price for all the securities is 100.
* Even though Python has problems with native threading (because of the GIL mechanism - watch first 4 minutes of [this](https://www.youtube.com/watch?v=Obt-vMVdM8s) video), for simplicity we'll use Python threads anyway. Similar architectural decisions in Java or C++ would not have this issue. We just assume there is no GIL in Python (the drawback is that if we try doing performance tests on this, the result will be inconsistent with what we would expect from C++/Java - other performance optimization techniques are required for Python - for, example, multiprocessing).
* Dummy price feed: shall be simplified to a separate thread going through each security one by one and incrementing its price.
* Dummy price calculation: one-liner in the code that has little meaning. The only requirements I set to the formula is to have it depending on all 4 arguments and bid should be lower than ask.
* Assuming that the request passed is always correct (that is security id and quantity are always numeric, the side is always BUY or SELL). Validation is omitted.
* Price storage (refer to implementation details for the reason there is a separate price storage) is just an array protected by a mutex. For the given particular case of security id range between 0 and 99 having an array is more efficient than using a map to store the price (considering no security ids will be added or removed, only values in the storage will be changed).

### Implementation Details
The reference price source is a separate independent thread, imitating an external price feed.

The price store is subscribing to the price feed. It is updated from reference price store thread and is not affecting other threads on the server. Read/write access to the price store is made thread safe since it will be accessed from multiple server threads.

Quoted price calculation is dependent on values that are available only at the moment it is being called (e. g., volume), so it can't be pre-calculated in a separate thread each time reference price update happens. Therefore, QuoteCalculationEngine is made to be just a utility class with price calculation being a static method.

The server needs to be efficient and handle many requests in the shortest time possible, therefore it makes sense to pre-create a thread pool that will be handling connections from clients.

There are only 2 test cases to verify the functionality. It is possible to make the data flow throughout the application deterministic and test for concrete values, but due to time constraint, only basic functionality is verified. Implementing test coverage report, though possible, not reasonable here due to the simplicity of the code.

Tests:
1. `test_reply_is_float` - just checks if the quoted price is a float and is within a sane interval.
2. `test_reply_many` does following:
  - starts multiple clients
  - makes sure they request the quoted price _without waiting for each previous client to complete_ (we need to make sure the test case is indeed multithreaded, not just imitating multithreading)
  - asserts the value requested (waiting for each client to complete the request during the assertion)
  - closes all connections and stops the server

### Running the App

* `server.py` - the server implementation (host and port are hardcoded on line 8)
* `tests/test_server.py` - test suite
* `get_prices.py` - a utility script that will start the quote server, request the bid and ask prices from the server for all securities and quantity 100 (reference prices are not deterministic here - reference price source runs without control) and print the result to _stdout_.   
