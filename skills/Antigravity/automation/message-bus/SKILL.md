---
name: message-bus
description: Design, configure, and orchestrate an asynchronous message bus for AI agent task delegation, with deterministic timestamp sorting, strict de-queuing, and one-to-many subscription broadcasts.
---

# Asynchronous AI Message Bus

## Goal
Provide robust rules, architectural guidance, and repeatable implementation patterns for an asynchronous AI message bus that resolves the structural boundary between a strict FIFO Queue and a broad Message Bus.

## When to Use This Skill
* Use this skill when designing or implementing asynchronous workflows where tasks need to be queued, ordered deterministically, and broadcasted to multiple active subscribers.
* Use this skill when resolving the structural boundary between a strict point-to-point FIFO Queue (optimal for simple task delegation) and a broad Message Bus Pattern (optimal when an initial task triggers secondary, decoupled actions).
* Use this skill to park a task into a message bus where different subagents or worker threads can process the task.

## Constraints & Rules
* **Task Ingestion:** Tasks must be added to a holding queue for addressing at a later operational step. The queueing mechanism must be non-blocking and must not lock the main execution thread.
* **Ordering & Identity Mechanics:** Every task payload must inject a distinct `timestamp` structural attribute into its identification schema. Deterministic ordering based on this `timestamp` must be enforced when sorting the current backlog queue.
* **Strict De-queuing Policy:** The exact moment a worker thread starts executing a task, that task must be actively removed from the active polling queue to prevent concurrent double-execution.
* **Subscription & Broadcast Model:** The core architecture must support a 1-to-many topology. Individual tasks must support registering multiple decoupled subscriber functions that hook into downstream action tasks.
* **Language:** ALL TEXT, NAMES, and CODE must be written in British English. Do not highlight this, just use the correct version of English (e.g. *behaviour*, *optimise*, *prioritise*, *initialise*, *de-queuing*, *analyse*).

## How to Use It

<Sequence>
  <Step title="Architectural Design" subtitle="Verify queue vs. message bus boundaries">
    Determine the workflow pattern. Choose a strict Queue Pattern for point-to-point worker delivery, or a Message Bus Pattern when a task completion triggers multiple decoupled downstream action tasks.
  </Step>
  <Step title="Asynchronous Ingestion" subtitle="Establish holding queue">
    Configure a non-blocking queueing interface. Ensure tasks can be appended to the backlog asynchronously without blocking the primary execution thread.
  </Step>
  <Step title="Deterministic Sorting" subtitle="Inject timestamps and order queue">
    Inject a distinct `timestamp` structural attribute into the payload identification schema of every task. Sort the holding queue deterministically based on this attribute (oldest timestamps first).
  </Step>
  <Step title="Concurrency Guarding" subtitle="Enforce de-queuing policy">
    Implement a strict de-queuing transition. The moment a worker thread claims and begins execution of a task, remove it from the active queue immediately to avoid concurrent double-execution.
  </Step>
  <Step title="1-to-Many Event Broadcast" subtitle="Dispatch completion events">
    Register decoupled subscriber functions to the task completion event. Once a task completes processing, broadcast the payload to all active subscribers to trigger downstream tasks.
  </Step>
</Sequence>

## Reference Examples

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
