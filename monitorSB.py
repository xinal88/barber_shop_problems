import threading
import time
import random

class BarberShop:
    def __init__(self, num_chairs):
        self.num_chairs = num_chairs
        self.waiting_customers = 0
        self.mutex = threading.Lock()
        self.customer_ready = threading.Condition(self.mutex)
        self.barber_ready = threading.Condition(self.mutex)

    def customer_arrives(self):
        with self.mutex:
            if self.waiting_customers < self.num_chairs:
                self.waiting_customers += 1
                print(f'Customer arrived. Waiting customers: {self.waiting_customers}')
                self.customer_ready.notify()  # Notify the barber that a customer is ready
            else:
                print('Customer leaves: no waiting chairs available.')

    def barber_cuts_hair(self):
        with self.mutex:
            while self.waiting_customers == 0:
                print('Barber is sleeping...')
                self.customer_ready.wait()  # Barber sleeps if there are no customers
            self.waiting_customers -= 1
            print(f'Barber is cutting hair. Waiting customers: {self.waiting_customers}')
            self.barber_ready.notify()  # Notify the customer that cutting is in progress

    def customer_done(self):
        with self.mutex:
            self.barber_ready.wait()  # Wait for the barber to finish cutting hair
            print('Customer is done and leaves.')

def customer_thread(barber_shop):
    barber_shop.customer_arrives()
    barber_shop.customer_done()

def barber_thread(barber_shop, running_event):
    while running_event.is_set():
        barber_shop.barber_cuts_hair()
        time.sleep(random.uniform(1, 3))  # Simulate time taken to cut hair

def main():
    num_chairs = 3
    barber_shop = BarberShop(num_chairs)

    # Create a threading event to control the barber's running state
    running_event = threading.Event()
    running_event.set()

    # Create barber thread
    barber = threading.Thread(target=barber_thread, args=(barber_shop, running_event))
    barber.start()

    # Create customer threads
    for _ in range(10):  # Create 10 customers
        time.sleep(random.uniform(0.1, 1))  # Random arrival times
        threading.Thread(target=customer_thread, args=(barber_shop,)).start()

    # Let the simulation run for a specified duration
    time.sleep(15)  # Run the simulation for 15 seconds

    # Signal the barber to stop running
    running_event.clear()
    barber.join()  # Wait for the barber thread to finish

    print("Simulation has ended.")

if __name__ == "__main__":
    main()