# Token Bucket
This algorithm is one of the most popular rate-limiting algorithms (used by 
companies like Amazon and Stripe) because it is memory-efficient and allows for
short bursts of traffic.
## Design
This is built using "**lazy evaluation.**" We only calculate how many tokens should
be added when a new request comes in based on the time that has elapsed since
the last request.
Mutex Lock is used to handle concurrency.
# Fixed Window Counter
In this algorithm, time is divided into fix-sized time windows (e.g. Window 1 is `10:00:00 to 10:00:05` while Window 2 is`10:00:05 to 10:00:10`) and a counter is assigned for each window.
The counter is incremented by 1 each time a request comes in. Omce the counter reaches a pre-defined limit, new requests are blocked until a new time window starts where the counter 
resets to 0.
