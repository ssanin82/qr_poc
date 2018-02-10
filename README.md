# Quote Server
## Requirements Summary
* Requests should be handled via TCP connections
* Can be more than one client
* Maximize throughput
* Minimize response time
* Request - single line: `{security ID} (BUY|SELL) {quantity}` (_security id_ and _quantity_ are integers) 
* Response - single line with a single numeric value representing the quoted price
* `QuoteCalculationEngine` and `ReferencePriceSource` - provided interfaces
