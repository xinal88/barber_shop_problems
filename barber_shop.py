import threading
import time
import random

#Define the maximum number of customers and the number of chairs in the waiting room
MAX_CUSTOMERS = 7
NUM_CHAIRS = 4
TIMEOUT = 5 #The maximum time that there is no customers (s)

#Define the semaphore for the barber, the customers, and the mutex
barber_semaphore = threading.Semaphore(0)
customer_semaphore = threading.Semaphore(0)
mutex = threading.Lock()

waiting_customers = [] #A list to keep track of the waiting customers

# The attending time of the last customer
last_customer_time = time.time()
running = True 

# Define the barber thread function
def barber():
    global last_customer_time, running
    while running:
        current_time = time.time()
        # Check if the waiting time is over the timeout
        if len(waiting_customers) == 0:
            if current_time - last_customer_time > TIMEOUT:
                print("Exceed the timeout (5s). The barber goes to bed. CLOSED\n")
                running = False
                break
            print("The Barber is sleeping\n")
            time.sleep(1)   # Reduce the frequency of check to 1 to preserve the resources
        else:
            print("Welcome to the barber!\n")
            barber_semaphore.acquire()
            mutex.acquire()
            if len(waiting_customers) > 0:
                customer = waiting_customers.pop(0)
                print(f"The barber is cutting hair for customer {customer}\n")
                mutex.release()
                time.sleep(random.randint(1,5))
                print(f"The barber has finished cutting hair for customer {customer}\n")
                customer_semaphore.release()
            else:
                mutex.release()

def customer(index):
    global waiting_customers, last_customer_time, running
    time.sleep(random.randint(1, 5))
    if running:
        mutex.acquire()
        if len(waiting_customers) < MAX_CUSTOMERS:
            waiting_customers.append(index)
            last_customer_time = time.time()    # Update the time of the last customer
            print(f"Customer {index} is waiting in the waiting room\n")
            mutex.release()
            barber_semaphore.release()
            customer_semaphore.acquire()
            print(f"Customer {index} has finished getting a haircut\n")
        else:
            print(f"Customer {index} is leaving because the waiting room is full\n")
            mutex.release()

# Create a thread for the barber
barber_thread = threading.Thread(target=barber)

# Create a thread for each customer
customer_threads = []
for i in range(MAX_CUSTOMERS):
    customer_threads.append(threading.Thread(target=customer, args=(i,)))

# Start the barber and customer threads
barber_thread.start()
for thread in customer_threads:
    thread.start()

# Wait for the customer threads to finish
for thread in customer_threads:
    thread.join()

# Wait for the barber thread to finish
barber_thread.join()

print("The barber store is closed. Thank you for using our service!\n")