import time
import threading


class TokenBucket:
    def __init__(self, capacity, refill_rate_per_sec):
        """Initialize class.

        Args:
            capacity: Maximum number of tokens the bucket can hold
            refill_rate_per_sec: Number of tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.bucket_tokens = capacity  # Bucket starts full
        self.last_refill_time = time.time()
        self.lock = threading.Lock()    # Lock for thread safety

    def _refill(self):
        """Calculate how much time elapsed since last request came in.
        Multiply that time by the refill rate to know how many tokens to be
        added to the bucket.
        """
        now = time.time()
        time_elapsed = now - self.last_refill_time

        # Calculate tokens to add based on elapsed time
        tokens_to_add = time_elapsed * self.refill_rate

        if tokens_to_add > 0:
            # Add tokens to bucket but don't exceed max capacity
            self.bucket_tokens = min(self.capacity, self.bucket_tokens + tokens_to_add)
            self.last_refill_time = now


    def allow_request(self, tokens_needed=1):
        """Method to be called when when a user makes an API request.
        It refills the bucket, check if there is enough tokens, and then deduct
        a token if allowed.

        Returns:
            True if request is allowed
            False if rate limit is exceeded (HTTP 429)
        """
        with self.lock: # Acquire lock before checking/modifying state
            self._refill()  # Refill bucket first based on elapsed time
            if self.bucket_tokens >= tokens_needed:
                self.bucket_tokens -= tokens_needed
                return True
            return False
