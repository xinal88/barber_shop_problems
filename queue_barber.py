import time
import queue
import threading
import random

# Define the maximum number of customers and the number of chairs in the waiting room
MAX_CUSTOMERS = 5  # Total customers to be served
NUM_CHAIRS = 3     # Chairs available in the waiting room

# Shared resource: queue of waiting customers
waiting_customers = queue.Queue(NUM_CHAIRS)
customer_served = 0
mutex = threading.Lock()
customer_ready = threading.Condition(mutex)

# Barber thread function
def barber():
    global customer_served
    while True:
        with customer_ready:
            while waiting_customers.empty():
                if customer_served == MAX_CUSTOMERS:
                    print("All customers have been served. The shop is closing.")
                    return
                print("The barber is sleeping...")
                customer_ready.wait()
            customer = waiting_customers.get()  # Get the first customer from the waiting room
        
        # Get the first customer from the waiting room
        print(f"The barber is cutting hair for customer {customer}")
        
        # Simulate the haircut time
        time.sleep(random.randint(1, 5))
        print(f"The barber has finished cutting hair for customer {customer}")
        
        # Signal the customer that their haircut is done
        waiting_customers.task_done()
        customer_served += 1

# Customer thread function
def customer(index):
    time.sleep(random.randint(1, 5))  # Simulate random arrival time
    
    with customer_ready:
        try:
            waiting_customers.put_nowait(index)  # Add customer to the waiting room
            print(f"Customer {index} is waiting in the waiting room")
            customer_ready.notify()
        except queue.Full:
            print(f"Customer {index} leaves because no chair is available.")

if __name__ == "__main__":
    threading.Thread(target=barber).start()

    for i in range(1, MAX_CUSTOMERS+1):
        threading.Thread(target=customer, args=(i,)).start()  # Pass the index as a single-element tuple
        time.sleep(random.uniform(0.1, 1.0))  # Simulate random arrival of customers