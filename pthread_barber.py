import threading
import time
import random

NUM_CHAIRS = 3          # Number of chairs in the waiting room
MAX_CUSTOMERS = 5       # Total number of customers to be served

mutex = threading.Lock()                # Mutex to control access to shared resources
customerReady = threading.Condition(mutex) # Condition to signal when a customer arrives
barberReady = threading.Condition(mutex)   # Condition to signal when the barber is ready

waiting_customers = 0                   # Current number of customers in the waiting room
total_customers_served = 0              # Total number of customers served

# Barber thread function
def barber():
    global waiting_customers, total_customers_served
    
    while True:
        with mutex:
            # Wait for customers to arrive
            while waiting_customers == 0:
                if total_customers_served == MAX_CUSTOMERS:
                    print("All customers have been served. The shop is closing.")
                    return
                print("The barber is sleeping...")
                customerReady.wait()  # Wait for a customer to signal arrival
            
            # A customer is ready; the barber will serve them
            waiting_customers -= 1
            print("The barber is cutting hair for a customer.")
            
            # Notify the customer that the barber is ready
            barberReady.notify()
        
        # Simulate haircut time outside the locked section
        time.sleep(random.randint(1, 3))
        
        with mutex:
            total_customers_served += 1
            print("The barber has finished cutting hair.")

# Customer thread function
def customer(customer_id):
    global waiting_customers
    
    time.sleep(random.randint(1, 5))  # Simulate random arrival time

    with mutex:
        if waiting_customers < NUM_CHAIRS:
            # Customer takes a seat in the waiting room
            waiting_customers += 1
            print(f"Customer {customer_id} is waiting in the waiting room.")
            
            # Notify the barber that a customer is ready
            customerReady.notify()
            
            # Wait until the barber is ready for them
            barberReady.wait()
            print(f"Customer {customer_id} is getting a haircut.")
        else:
            # No available chair, customer leaves
            print(f"Customer {customer_id} leaves because no chair is available.")

if __name__ == "__main__":
    # Start the barber thread
    threading.Thread(target=barber).start()

    # Start customer threads
    for i in range(1, MAX_CUSTOMERS + 1):
        threading.Thread(target=customer, args=(i,)).start()
        time.sleep(random.uniform(0.1, 1.0))  # Random arrival of customers
