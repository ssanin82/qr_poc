# Quote Server
## Requirements Summary
* Requests should be handled via TCP connections
* Can be more than one client
* Maximize throughput and minimize response time (assume quoted price calculation may take long time to complete)
* Request - single line: `{security ID} (BUY|SELL) {quantity}` (security id and quantity are integers) 
* Response - single line with a single numeric value representing the quoted price
* Suggested interfaces: `QuoteCalculationEngine::calculate_quote_price(sec_id, ref_price, buy, qty)`, `ReferencePriceSource::subscribe(listener)`, `ReferencePriceSource::get(sec_id)`, `ReferencePriceSourceListener::reference_price_changed(sec_id, price)`

## Assumptions and Simplifications
* We have a fixed number of securities with their ids ranging from 0 to 99. Initial price for all securities is 100.
* Even though Python has problems with native threading (because of the GIL mechanism), for simplicity we'll use Python thread here anyway. Definitely, should this be written in Java or C++, similar architecture would not have this issue.
* Dummy price feed: TODO
* Dummy price calculation: TODO
* Assuming that request passed is always correct (that is security id and quantity are always numeric, side is always BUY or SELL)
* Price storage is just an array protected by a mutex. For the given particular case of security id range between 0 and 99 this is a bit faster than a map (considering no security ids will be added or removed)

## Architectural Decisions
* We can't pre-calculate the requested price in a separate thread and return the value on request because the calculation depends on quantity which is known only at the time of the request. Hence, a way to speed up response time and
* TODO describe interface changes (no get in ReferencePriceSource)

## TODO
* Decide on price calculation algorithm
* Stress tests
* Grammarly
