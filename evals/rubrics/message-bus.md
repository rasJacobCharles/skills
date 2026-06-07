# Asynchronous AI Message Bus Rubric

Score each criterion **PASS (1)** / **FAIL (0)** / **N/A**.
N/A criteria are excluded from the denominator.
Final score = sum(PASS) / sum(applicable) × 100.

---

## 1. Task Ingestion (C1)
*   **1.1** Demonstrates that tasks are queued asynchronously without locking or blocking the main execution thread.
*   **1.2** Explains how tasks are parked in a temporary or persistent holding queue before execution.

## 2. Ordering & Identity Mechanics (C2)
*   **2.1** Injects a distinct `timestamp` structural attribute into the identification schema of every task payload.
*   **2.2** Sorts the backlog queue deterministically based on the `timestamp` attribute, even when tasks are received out of order.

## 3. Lifecycle Management (C3)
*   **3.1** Enforces a strict de-queuing policy where a task is immediately removed from the active queue the moment execution begins.
*   **3.2** Proves that concurrent double-execution of a task by multiple worker threads is prevented.

## 4. Subscription & Broadcast Model (C4)
*   **4.1** Implements a 1-to-many subscription topology for completion event broadcasts.
*   **4.2** Demonstrates that multiple active subscribers receive the event broadcast successfully when a parent task completes.
