import time
import threading


class LeakingBucket:
    def __init__(self, capacity, leak_rate_per_sec):
        """Initialize class.

        Args:
            capacity: Maximum water (requests) the bucket can hold can hold
            leak_rate_per_sec: Number of requests processed per second
        """
        self.capacity = capacity
        self.leak_rate = leak_rate_per_sec
        self.current_water = 0  # Bucket starts empty
        self.last_leak_time = time.time()
        self.lock = threading.Lock()

    def _leak(self):
        now = time.time()
        time_elapsed = now - self.last_leak_time

        # Calculate how much water leaked out over time
        water_leaked = time_elapsed * self.leak_rate

        if water_leaked > 0:
            # Water level drops but can never go below 0 (empty)
            self.current_water = max(0, self.current_water - water_leaked)
            self.last_leak_time = now

    def allow_request(self):
        with self.lock:
            self._leak()    # Let the bucket leak first

            # If the bucket is not overflowing, accept the request else drop it
            if self.current_water + 1 < self.capacity:
                self.current_water += 1 # Add a drop of water
                return True
            return False
