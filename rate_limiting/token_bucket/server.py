from flask import Flask, request, jsonify
import time
import threading


app = Flask(__name__)

class TokenBucket:

    def __init__(self, capacity, refill_rate_per_sec):
        """Initialize class.

        Args:
            capacity: Maximum number of tokens the bucket can hold
            refill_rate_per_sec: Number of tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.current_tokens = capacity  # Bucket starts full
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
            self.current_tokens = min(self.capacity, self.current_tokens + tokens_to_add)
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

            if self.current_tokens >= tokens_needed:
                self.current_tokens -= tokens_needed
                return True
            return False


# --- Rate Limiter Manager ---
# This dictionary stores a bucket for each user: {"florence": TokenBucket(),
# "emmanuella": TokenBucket()}
user_buckets = {}
bucket_creation_lock = threading.Lock() # Prevents race conditions when creating new users

def get_rate_limiter(user_id):
    with bucket_creation_lock:
        if user_id not in user_buckets:
            # Give a first-timer a bucket (e.g. 5 capacity, 1 token/sec)
            user_buckets[user_id] = TokenBucket(capacity=5, refill_rate_per_sec=1)
        return user_buckets[user_id]
        
# --- API Endpoint ---
@app.route('/api/data', methods=['GET'])
def get_data():
    """Get user_id from query parameters (e.g. /api/data?user_id=alice)
    Defaults to 'anonymous' if no user_id is provided.
    """
    user_id = request.args.get('user_id', 'anonymous')

    # Get specific rate limiter for this user
    limiter = get_rate_limiter(user_id)

    if limiter.allow_request():
        # HTTP OK
        return jsonify({"status": "Success", "data": "Here is your protected data!"})
    else:
        # HTTP 429 Too Many Requests
        return jsonify({"status": "Error",
                        "message": "Rate limit exceeded. Try again later."}), 429
    
if __name__ == '__main__':
    # Run the server on port 5000
    print("Starting API Server on http://localhost:5000...")
    app.run(port=5000, debug=False)
