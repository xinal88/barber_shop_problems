import time
import random
import threading
from collections import deque

class BarberShopFSM:
    def __init__(self, max_chairs, operating_time):
        self.state = "Sleeping"        # Initial state
        self.queue = deque()           # Queue for waiting customers
        self.max_chairs = max_chairs   # Maximum number of chairs in the waiting area
        self.wait_start_time = None    # To track waiting time in the Waiting state
        self.operating_time = operating_time  # Total operating time before closing
        self.start_time = time.time()         # Record the start time
        self.is_open = True                   # Shop is initially open
        self.lock = threading.Lock()          # Lock to control state changes
        self.shop_closed = False              # Flag to signal the shop has completed all tasks

    def customer_arrives(self):
        with self.lock:
            if not self.is_open:
                print("Shop is closed to new customers. Customer leaves.")
                return

            print("Customer arrives.")
            if self.state == "Sleeping":
                self.state = "Cutting Hair"
                print("Barber wakes up and starts cutting hair.")
            elif self.state == "Waiting":
                self.state = "Cutting Hair"
                print("Barber stops waiting and starts cutting hair for the new customer.")
            elif len(self.queue) < self.max_chairs:
                self.queue.append("Customer")  # Add customer to the queue
                print(f"Customer added to the queue. Waiting customers: {len(self.queue)}/{self.max_chairs}")
            else:
                print("No available chairs. Customer leaves.")

    def service_complete(self):
        with self.lock:
            if self.queue:
                print("Next customer starts haircut.")
                self.queue.popleft()  # Remove one customer from the queue
                self.state = "Cutting Hair"
            else:
                if not self.is_open:
                    # No more customers and shop is closed: Set shop_closed to True
                    self.shop_closed = True
                    print("Barber shop is closed and all customers are served.")
                else:
                    print("No more customers; barber goes to waiting.")
                    self.state = "Waiting"
                    self.wait_start_time = time.time()  # Start the waiting timer

    def check_timeout(self):
        """Check if the barber has been waiting for over 5 seconds without a new customer."""
        with self.lock:
            if self.state == "Waiting" and self.wait_start_time:
                elapsed_time = time.time() - self.wait_start_time
                if elapsed_time > 5:
                    print("Timeout exceeded. No customers arrived. Barber goes to sleep.")
                    self.state = "Sleeping"
                    self.wait_start_time = None  # Reset wait timer

    def check_closing_time(self):
        """Check if the barber shop has reached its closing time."""
        with self.lock:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > self.operating_time:
                self.is_open = False
                print("The barber shop is now closed to new customers.")

    def run(self):
        """Simulate the barber shop operations in a loop."""
        while not self.shop_closed:
            self.check_closing_time()  # Check if shop should close to new customers

            with self.lock:
                if self.state == "Sleeping":
                    print("Barber is sleeping.")
                    time.sleep(2)  # Wait for the next event (customer arrival)
                elif self.state == "Cutting Hair":
                    print("Barber is cutting hair.")
                elif self.state == "Waiting":
                    print("Barber is waiting for a customer.")

            # Handle each state outside the lock to avoid deadlock with time.sleep
            if self.state == "Cutting Hair":
                time.sleep(3)  # Simulate time taken to cut hair
                self.service_complete()
            elif self.state == "Waiting":
                time.sleep(1)  # Check periodically
                self.check_timeout()

def simulate_random_customers(barber_shop):
    """Function to simulate random customer arrivals with varied intervals."""
    while barber_shop.is_open:
        # Random delay between 1 and 10 seconds to create varied situations
        time.sleep(random.uniform(1, 5))
        barber_shop.customer_arrives()

# Initialize barber shop with a maximum of 3 chairs and set to close after 30 seconds
barber_shop = BarberShopFSM(max_chairs=3, operating_time=30)

# Run the barber shop FSM in a separate thread
barber_shop_thread = threading.Thread(target=barber_shop.run)
barber_shop_thread.start()

# Start simulating random customer arrivals
simulate_random_customers(barber_shop)

# Wait for the barber shop to complete serving all customers
barber_shop_thread.join()
print("Barber shop simulation has finished.")
