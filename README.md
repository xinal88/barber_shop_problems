# Barber Shop Problem in Operating Systems

## Overview

The Barber Shop problem is a classic synchronization problem in operating systems, illustrating the challenges of managing shared resources between multiple threads. In this problem, we simulate a barber shop where a barber serves customers in a waiting room. If no customers are present, the barber sleeps until a new customer arrives. This implementation is written in Python and utilizes threading and synchronization mechanisms to demonstrate the solution.

## Problem Description

The barber shop has:
1. **One Barber** who cuts customers' hair.
2. **A Waiting Room** with a limited number of seats.
3. **Multiple Customers** who come to the barber shop.

### Rules
- If the barber is busy, customers wait in the waiting room.
- If all seats are occupied, customers leave.
- If the barber has no customers, he goes to sleep.
- When a customer arrives, they either take a seat (if available) or wake up the barber.

## Implementation

This solution is implemented in Python using:
- **Threads** to simulate the barber and customer actions.
- **Locks/Conditions** to synchronize the access to the barber's chair and waiting room seats.
  
### Requirements

- Python 3.6+
- Required libraries:
  - `threading` (part of the Python standard library)
  - `time` (for sleep simulation)

### Files
- `barber_shop.py`: Contains the main code for the Barber Shop problem simulation.
- `README.md`: Documentation (this file).

## How to run the program

1. **Clone the repository or download the code files:**
   ```bash
   git clone https://github.com/your-username/barber-shop-problem.git
   ```
2. **Navigate to the project directory:**
   ```
   cd barber-shop-problem
   ```
3. **Run the code:**
   ```
   python barber_shop.py
   ```
