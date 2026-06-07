---
name: message-bus
description: Design, configure, and orchestrate an asynchronous message bus for AI agent task delegation, with deterministic timestamp sorting, strict de-queuing, and one-to-many subscription broadcasts.
---

# Custom Harness Asynchronous AI Message Bus Skill

This skill provides robust rules, architectural guidance, and repeatable implementation patterns for an asynchronous AI message bus in custom LLM orchestration frameworks and harnesses. It resolves the structural boundary between a strict FIFO Queue and a broad Message Bus.

---

## 🎯 Core Principles

1. **Non-Blocking Ingestion:** Ingest tasks into the holding queue asynchronously. The ingestion mechanism must never lock or block the harness's main execution thread.
2. **Deterministic Backlog Sorting:** Inject a distinct `timestamp` structural attribute into the payload identification schema of every task. The holding queue must be sorted deterministically by this timestamp to handle out-of-order variations.
3. **Strict De-queuing:** Actively remove a task from the active polling queue at the exact moment a worker starts executing it. This concurrency guard prevents concurrent double-execution.
4. **1-to-Many Decoupled Broadcast:** Support a 1-to-many topology where multiple subscriber functions can hook into task completion events to run downstream action tasks asynchronously.

---

## 🧭 Workflow Phases

### Phase 1: Ingestion & Identification
1. Receive task requests from clients or internal modules.
2. Enforce the injection of a distinct `timestamp` attribute into the task payload.
3. Push the task payload asynchronously to the holding queue.

### Phase 2: Backlog Sorting
1. Sort the holding queue deterministically in ascending order of task timestamps.
2. Ensure that out-of-order task arrivals are resolved by the timestamp sorting algorithm.

### Phase 3: Claiming & Execution (De-queuing)
1. When a worker thread claims a task, execute the de-queuing policy immediately: remove the task from the holding queue.
2. Hand off the task payload to the worker thread for execution.
3. Prevent other workers from accessing or double-executing the claimed task.

### Phase 4: Event Broadcast
1. Upon task completion, broadcast the completion event to all registered subscriber callbacks concurrently.
2. Execute the downstream action tasks asynchronously.

---

## 🏛️ Reference Examples

### Example: Asynchronous Message Bus Implementation (TypeScript)
Below is an example of an asynchronous message bus implementing deterministic timestamp sorting, non-blocking ingestion, strict de-queuing, and 1-to-many event broadcasting.

```typescript
interface TaskPayload {
  id: string;
  timestamp: number; // Injected structural attribute for deterministic sorting
  data: any;
}

type Subscriber = (task: TaskPayload) => Promise<void>;

class AsyncMessageBus {
  private holdingQueue: TaskPayload[] = [];
  private subscribers: Map<string, Subscriber[]> = new Map();
  private isProcessing = false;

  // 1. Non-blocking Task Ingestion
  public async enqueueTask(task: Omit<TaskPayload, 'timestamp'>): Promise<void> {
    const enrichedTask: TaskPayload = {
      ...task,
      timestamp: Date.now(), // Auto-inject distinct timestamp attribute
    };
    
    // Asynchronous non-blocking push
    setImmediate(() => {
      this.holdingQueue.push(enrichedTask);
      this.sortQueue();
    });
  }

  // 2. Deterministic Ordering
  private sortQueue(): void {
    this.holdingQueue.sort((a, b) => a.timestamp - b.timestamp);
  }

  // 3. Strict De-queuing Policy & Lifecycle Management
  public async processNextTask(): Promise<void> {
    if (this.holdingQueue.length === 0 || this.isProcessing) return;
    this.isProcessing = true;

    // Strict De-queuing: remove from queue immediately at execution start
    const activeTask = this.holdingQueue.shift();
    if (!activeTask) {
      this.isProcessing = false;
      return;
    }

    try {
      await this.executeTask(activeTask);
      await this.broadcastCompletion(activeTask);
    } finally {
      this.isProcessing = false;
      // Triggers processing of the next sorted task
      setImmediate(() => this.processNextTask());
    }
  }

  private async executeTask(task: TaskPayload): Promise<void> {
    // Simulate task execution
    return new Promise((resolve) => setTimeout(resolve, 50));
  }

  // 4. Subscription & Broadcast Model (1-to-many topology)
  public registerSubscriber(taskId: string, subscriber: Subscriber): void {
    if (!this.subscribers.has(taskId)) {
      this.subscribers.set(taskId, []);
    }
    this.subscribers.get(taskId)!.push(subscriber);
  }

  private async broadcastCompletion(task: TaskPayload): Promise<void> {
    const list = this.subscribers.get(task.id) || [];
    // Broadcast concurrently to all decoupled action tasks
    await Promise.all(list.map(subscriber => subscriber(task)));
  }
}
```
