"""File that uses threads to simulate users making requests at the exact same time.
"""
import requests
import time
import threading


def simulate_user_traffic(user_id):
    url = f"http://localhost:5000/api/data?user_id={user_id}"
    print(f"[{user_id.upper()}] Starting burst traffic...")

    # Send 7 requests rapidly
    for i in range(1, 8):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"[{user_id.upper()}] Request {i}: [200 OK]")
            elif response.status_code == 429:
                print(f"[{user_id.upper()}] Request {i}: [429 RATE LIMITED]")
            else:
                print(f"[{user_id.upper()}] Request {i}: [{response.status_code}]")
        except requests.exceptions.ConnectionError:
            print("Server is not running! Please start server.py")
            return
        
        # Slight delay
        time.sleep(0.05)


if __name__ == "__main__":
    print("============ Starting Multi-User Simulation ==============\n")

    # Threads representing different users
    oluchi_thread = threading.Thread(target=simulate_user_traffic, args=("oluchi",))
    alice_thread = threading.Thread(target=simulate_user_traffic, args=("alice",))
    unwana_thread = threading.Thread(target=simulate_user_traffic, args=("unwana",))
    esther_thread = threading.Thread(target=simulate_user_traffic, args=("esther",))
    chidinma_thread = threading.Thread(target=simulate_user_traffic, args=("chidinma",))

    # Start the threads at the same time
    oluchi_thread.start()
    alice_thread.start()
    unwana_thread.start()
    esther_thread.start()
    chidinma_thread.start()

    # Wait for the users to finish their traffic bursts
    oluchi_thread.join()
    alice_thread.join()
    unwana_thread.join()
    esther_thread.join()
    chidinma_thread.join()

    print("============ Test Complete ===============")
