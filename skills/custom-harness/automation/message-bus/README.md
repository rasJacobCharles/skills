# Asynchronous AI Message Bus Skill

This folder contains the **Asynchronous AI Message Bus** skill for AI coding assistants. It provides robust rules, architectural guidance, and repeatable implementation patterns to queue tasks, order them deterministically, and broadcast them to multiple active subscribers.

---

## 🏛️ Design Philosophies

This skill defines a robust template for building asynchronous message bus workflows using four key principles:

### 1. Non-Blocking Task Ingestion
To keep the main execution thread free, tasks are ingested asynchronously into a holding queue. This ensures that scheduling and parking tasks do not lock the primary application loop.

### 2. Deterministic Timestamp Sorting
Every task payload must inject a distinct `timestamp` structural attribute into its identification schema. The holding queue is then sorted deterministically based on this attribute, ensuring that tasks are processed in a predictable order regardless of arrival timing.

### 3. Strict De-queuing Policy
To prevent concurrent double-execution by multiple worker threads, a task is actively removed from the active queue at the exact moment execution starts.

### 4. Decoupled 1-to-Many Subscription Topology
The message bus supports registering multiple subscriber functions to tasks. When a task completes execution, its completion event is broadcasted to all registered subscribers to trigger downstream actions.

---

## 📂 Folder Structure

```text
message-bus/
├── README.md                 # This human-readable guide
├── SKILL.md                  # Main router and bus execution protocol
└── eval.md                   # Evaluation configuration (points to central fixtures & rubrics)
```

---

## 🧭 How the Message Bus Operates (Execution Protocol)

1. **Ingress**: A client or worker requests task execution, supplying a payload.
2. **Identification & Injection**: The message bus receives the payload and injects a distinct `timestamp` attribute.
3. **Deterministic Queueing**: The task is appended to the holding queue asynchronously. The queue is immediately sorted in ascending order of task timestamps.
4. **De-queuing & Processing**:
   *   A worker thread requests the next task.
   *   The bus removes the oldest task from the queue immediately upon worker pickup to prevent double-execution.
   *   The worker executes the task payload.
5. **Broadcasting**: Upon completion, the bus broadcasts the completion event to all registered subscriber callbacks, initiating downstream action tasks.

---

## 🧪 Running Evaluations

To verify that the agent conforms to this execution protocol, run the self-scoring evaluation command from your workspace:

```bash
/eval custom-harness/message-bus
```

This runs synthetic fixtures (ingestion, sorting, de-queuing, and broadcasting) and scores them against the shared rubric.
