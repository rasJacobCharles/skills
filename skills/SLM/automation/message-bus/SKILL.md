---
name: message-bus
description: Design, configure, and orchestrate an asynchronous message bus for AI agent task delegation, with deterministic timestamp sorting, strict de-queuing, and one-to-many subscription broadcasts.
---

# SLM Asynchronous AI Message Bus Skill (Optimized)

Use this skill when running a Small Language Model (SLM) under 10B parameters. Keep context small and follow these instructions strictly.

---

## 🚨 SYSTEM CONSTRAINTS (CRITICAL)

1. **DO NOT WRITE CODE** unless explicitly requested by the user.
2. **NON-BLOCKING INGESTION:** Queuing tasks must be asynchronous and must not block the main execution thread.
3. **DETERMINISTIC ORDERING:** Every task payload must inject a distinct `timestamp` attribute. The queue must sort tasks deterministically based on this attribute.
4. **STRICT DE-QUEUING:** Tasks must be removed from the active queue immediately upon starting execution to prevent concurrent double-execution.
5. **1-TO-MANY BROADCAST:** Support registering multiple subscribers and broadcasting task completion events to all of them.

---

## 🧭 WORKFLOW

### Phase 1: Ingest Tasks
* Ingest task requests asynchronously.
* Append them to the holding queue without blocking the main event loop.

### Phase 2: Inject Identity & Sort
* Inject a distinct `timestamp` structural attribute into the payload identification schema of every task.
* Sort the holding queue in ascending order of timestamps (oldest task first).

### Phase 3: Claim & De-queue
* The moment a worker thread starts executing a task, remove it from the active queue immediately to prevent double-execution.

### Phase 4: Broadcast Events
* Once execution completes, broadcast the event to all registered subscriber callbacks in a 1-to-many topology.

---

## 🗂️ FILE STRUCTURE

The in-memory or on-disk architecture must model:
*   **holdingQueue:** Array of task payloads sorted deterministically.
*   **taskPayload:** Includes `id`, `timestamp`, and `data` attributes.
*   **subscribers:** Map matching task IDs to arrays of subscriber callbacks.

---

## ⚙️ SCRIPT UTILITIES

### Example: Asynchronous Message Bus Implementation (TypeScript)

```typescript
interface TaskPayload {
  id: string;
  timestamp: number;
  data: any;
}

type Subscriber = (task: TaskPayload) => Promise<void>;

class AsyncMessageBus {
  private holdingQueue: TaskPayload[] = [];
  private subscribers: Map<string, Subscriber[]> = new Map();
  private isProcessing = false;

  public async enqueueTask(task: Omit<TaskPayload, 'timestamp'>): Promise<void> {
    const enrichedTask: TaskPayload = { ...task, timestamp: Date.now() };
    setImmediate(() => {
      this.holdingQueue.push(enrichedTask);
      this.holdingQueue.sort((a, b) => a.timestamp - b.timestamp);
    });
  }

  public async processNextTask(): Promise<void> {
    if (this.holdingQueue.length === 0 || this.isProcessing) return;
    this.isProcessing = true;

    const activeTask = this.holdingQueue.shift();
    if (!activeTask) {
      this.isProcessing = false;
      return;
    }

    try {
      await this.executeTask(activeTask);
      const list = this.subscribers.get(activeTask.id) || [];
      await Promise.all(list.map(subscriber => subscriber(activeTask)));
    } finally {
      this.isProcessing = false;
      setImmediate(() => this.processNextTask());
    }
  }

  private async executeTask(task: TaskPayload): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, 50));
  }

  public registerSubscriber(taskId: string, subscriber: Subscriber): void {
    if (!this.subscribers.has(taskId)) this.subscribers.set(taskId, []);
    this.subscribers.get(taskId)!.push(subscriber);
  }
}
```
