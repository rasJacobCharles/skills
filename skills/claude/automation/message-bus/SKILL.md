---
name: message-bus
description: Design, configure, and orchestrate an asynchronous message bus for AI agent task delegation, with deterministic timestamp sorting, strict de-queuing, and one-to-many subscription broadcasts.
# disable-model-invocation: false
# user-invocable: true
---

# Asynchronous AI Message Bus

## Overview
This skill provides robust rules, architectural guidance, and repeatable implementation patterns for an asynchronous AI message bus. It resolves the structural boundary between a strict FIFO Queue and a broad Message Bus by establishing deterministic ordering and decoupled pub/sub execution.

## Purpose & Scope
* **When to use:**
  * Use when designing asynchronous agentic workflows where tasks must be queued and processed asynchronously by independent subagents.
  * Use when tasks need to be ordered deterministically based on creation timestamps, regardless of physical network arrival sequence.
  * Use when task completion must trigger multiple decoupled downstream actions across separate worker modules.
* **When NOT to use:**
  * Do not use for simple, synchronous, single-task execution paths that have no downstream dependencies or concurrency requirements.
  * Do not use for strict point-to-point worker delivery where task execution ordering is unimportant.

## Step-by-Step Instructions

<Sequence>
  <Step title="Analyse Workflow Suitability" subtitle="Identify boundary conditions">
    Evaluate if the workflow requires a strict Queue Pattern (point-to-point single execution) or a Message Bus Pattern (event-driven pub/sub for downstream actions).
  </Step>
  <Step title="Configure Queueing Ingestion" subtitle="Establish holding queue">
    Implement a non-blocking queueing interface to ingest tasks asynchronously without locking the main execution thread.
  </Step>
  <Step title="Enforce Deterministic Ordering" subtitle="Inject timestamps">
    Ensure each task payload has a distinct `timestamp` attribute injected into its schema. Sort the queue in ascending order of timestamps.
  </Step>
  <Step title="Apply Concurrency Guardrails" subtitle="Implement de-queuing policy">
    Enforce immediate task removal from the active queue at the exact moment execution starts, preventing concurrent double-execution by other worker threads.
  </Step>
  <Step title="Bind Downstream Subscribers" subtitle="Orchestrate 1-to-many broadcast">
    Register decoupled subscriber functions to completion events and broadcast the event concurrently to all active subscribers when a task completes.
  </Step>
</Sequence>

## Output Format
* **Style:** Technical design blueprints, specifying schema structures and operational logic.
* **Structure:** Provide code schemas and flow diagrams mapping the queue mechanics, lifecycle transitions, and subscriber bindings.

## Guardrails & Anti-Patterns
* **Critical Constraint:** Never permit a task to remain in the active queue once a worker starts processing it.
* **Critical Constraint: ALL TEXT and NAMES, CODE for things must be written in British English. Do not highlight this, just use the correct version of English.**
* **Avoid:** Do not use blocking operations for enqueueing tasks.
* **Avoid:** Do not run subscriber actions synchronously in a way that blocks the message bus completion phase.

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
