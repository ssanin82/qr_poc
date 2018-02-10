# Quote Server
## Requirements Summary
* Requests should be handled via TCP connections
* Can be more than one client
* Maximize throughput and minimize response time (assume quoted price calculation may take long time to complete)
* Request - single line: `{security ID} (BUY|SELL) {quantity}` (_security id_ and _quantity_ are integers) 
* Response - single line with a single numeric value representing the quoted price
* Suggested interfaces: `QuoteCalculationEngine::calculate_quote_price(sec_id, ref_price, buy, qty)`, `ReferencePriceSource::subscribe(listener)`, `ReferencePriceSource::get(sec_id)`, `ReferencePriceSourceListener::reference_price_changed(sec_id, price)`

## Assumptions and Simplifications
* We have a fixed number of securities with their ids ranging from 0 to 99
* Even though Python has problems with native threading (because of the GIL mechanism), for simplicity we'll use Python thread here anyway. Definitely, should this be written in Java or C++, similar architecture would not have this issue.
* Dummy price feed: TODO
* Dummy price calculation: TODO

## TODO
* Decide on price calculation algorithm
* Stress tests
