import requests
import time
import threading


def simulate_user_traffic(user_id):
    url = f"http://localhost:5000/api/data?user_id={user_id}"
    print(f"[{user_id.upper()}] Starting burst traffic...")

    # Sending 7 requests rapidly
    for i in range(1, 8):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"[{user_id.upper()}] Request {i}: [200 OK]")
            elif response.status_code == 429:
                print(f"[{user_id.upper()}] Request {i}: [429 RATE LIMITED]")
        except requests.exceptions.ConnectionError:
            print("Server is not running, start server.py")
            return
        # Minor delay    
        time.sleep(0.05)


if __name__ == '__main__':
    # Create separate "browser" threads for ALice, Unwana, and Oluchi
    alice_thread = threading.Thread(target=simulate_user_traffic, args=("alice",))
    unwana_thread = threading.Thread(target=simulate_user_traffic, args=("unwana",))
    oluchi_thread = threading.Thread(target=simulate_user_traffic, args=("oluchi",))

    # Start threads at the exact same time
    alice_thread.start()
    unwana_thread.start()
    oluchi_thread.start()

    # Wait for threads to terminate
    alice_thread.join()
    unwana_thread.join()
    oluchi_thread.join()

    print("\n========= Test Complete =========")
