from flask import Flask, request, jsonify
from token_bucket import TokenBucket
from leaking_bucket import LeakingBucket
import threading


app = Flask(__name__)

user_buckets = {}
bucket_creation_lock = threading.Lock()

def get_rate_limiter(user_id):
    """Rate limiter manager."""
    with bucket_creation_lock:
        if user_id not in user_buckets:
            # UNCOMMENT ALGORITHM TO TEST:
            # user_buckets[user_id] = TokenBucket(capacity=5, refill_rate_per_sec=1)
            user_buckets[user_id] = LeakingBucket(capacity=5, leak_rate_per_sec=1)

            return user_buckets[user_id]
        
# API Endpoint
@app.route('/api/data', methods=['GET'])
def get_data():
    user_id = request.args.get('user_id', 'anonymous')
    limiter = get_rate_limiter(user_id)

    if limiter.allow_request():
        return jsonify({"status": "Success", "data": "Here lies a protected data!"}), 200
    else:
        return jsonify({"status": "Error", "message": "Rate limit exceeded. Try again later."}), 429
    

if __name__ == "__main__":
    print("Starting API Server...")
    app.run(port=5000, debug=False)
