# Application of Finite State Machine (FSM) in the Barber Shop Code
In this simulation, the barber shop operates as a Finite State Machine (FSM). An FSM is a computational model used to represent and manage states and transitions based on inputs or events. Here, the barber's actions are modeled through different states, with transitions occurring based on customer arrivals, service completions, and waiting timeouts. This approach effectively controls the flow of the simulation and allows for structured, predictable state changes.

## Key FSM Components in the Barber Shop Simulation
### **States:**

**Sleeping:** The barber is not cutting hair and has no customers. This is the initial state, where the barber waits until a customer arrives.
**Cutting Hair:** The barber is actively cutting hair for a customer. When a customer is in service, the barber remains in this state until the haircut is finished.
**Waiting:** The barber has finished a haircut but finds the queue empty. In this state, the barber waits for new customers. If no new customer arrives within a timeout period (5 seconds), the barber transitions to the Sleeping state.
### **Transitions:**

**Customer Arrives:**
If the barber is in the Sleeping state, the state changes to Cutting Hair, as the barber wakes up to serve the new customer.
If the barber is in the Waiting state, the state also changes to Cutting Hair, as the barber starts serving the newly arrived customer.
If the barber is already in Cutting Hair, the customer joins the queue if a chair is available; otherwise, the customer leaves due to a lack of available chairs.

**Service Complete:**
When the barber finishes cutting hair, they check the queue. If there are customers waiting, the barber remains in the Cutting Hair state, transitioning to the next customer.
If the queue is empty and the shop is still open, the barber transitions to the Waiting state. If the queue is empty and the shop has closed to new customers, the barber stops accepting new customers, eventually allowing the program to terminate.

**Timeout in Waiting:**
If the barber is in the Waiting state but no customers arrive within 5 seconds, the barber transitions to the Sleeping state.

**FSM Control Flow:**
The main run() function in BarberShopFSM acts as the central control loop, repeatedly checking the current state and executing actions accordingly. This loop ensures the barber follows a structured process, transitioning between states in response to events like customer arrivals or service completions.
Advantages of Using FSM in this Simulation

**Clarity and Predictability:**
Using FSM makes the barber’s actions clear and easy to follow. Each state represents a specific action, and transitions define precise conditions for moving between states. This structured approach avoids ambiguity and simplifies the control flow.

**Concurrency Management:**
FSM, combined with threading and locks, allows for controlled interactions between the barber and customers. Locks ensure that state transitions occur safely, even when multiple threads are active, and the barber’s actions remain consistent and accurate.

**Resource Optimization:**
The FSM model manages customer flow efficiently, respecting the constraints of limited chairs. By systematically checking the queue and only accepting customers if there’s space, it simulates real-world scenarios where resources are limited, a common case in service-based applications.
Controlled Termination:

FSM makes it easy to define and control termination criteria for the simulation. By setting shop_closed to True when all customers are served, the FSM model gracefully completes operations without leaving resources active unnecessarily.