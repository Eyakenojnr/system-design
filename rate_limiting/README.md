# Token Bucket
This algorithm is one of the most popular rate-limiting algorithms (used by 
companies like Amazon and Stripe) because it is memory-efficient and allows for
short bursts of traffic.
## Design
This is built using "**lazy evaluation.**" We only calculate how many tokens should
be added when a new request comes in based on the time that has elapsed since
the last request.
Mutex Lock is used to handle concurrency.

