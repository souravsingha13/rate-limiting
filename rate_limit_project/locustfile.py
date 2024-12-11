from locust import HttpUser, task, between
import random
import time

class RateLimitUser(HttpUser):
    # Define the minimum and maximum wait times between requests.
    wait_time = between(1, 3)

    @task
    def rate_limit(self):
        # Simulate making a request to the rate-limited endpoint
        response = self.client.get("/rate_limit/")
        print(response.json())  # Print the response for debugging

        # Here, we can check for rate limiting response (e.g., status 429)
        if response.status_code == 429:
            print("Rate limit exceeded!")
        
        # Optional: Introduce random sleep between requests
        time.sleep(random.randint(1, 2))  # Simulate thinking time

