\# Design Document: Vector Clocks vs CRDTs



\## 📌 Introduction



This project implements a multi-master replication system where multiple nodes (US, EU, APAC) can independently update the same data. The main challenge in such systems is handling \*\*concurrent updates and conflicts\*\* while ensuring eventual consistency.



To solve this, we used \*\*Vector Clocks\*\* for conflict detection and \*\*Last-Write-Wins (LWW)\*\* for conflict resolution.



\---



\## 🧠 Why Vector Clocks Were Chosen



Vector clocks are a \*\*state-based mechanism\*\* used to track the causal relationship between events in distributed systems.



\### Key Reasons:



1\. \*\*Causality Tracking\*\*



&#x20;  \* Vector clocks help determine whether:



&#x20;    \* One update happened before another

&#x20;    \* Updates are concurrent

&#x20;  \* This is essential in multi-master systems.



2\. \*\*Accurate Conflict Detection\*\*



&#x20;  \* Unlike timestamps, vector clocks do not rely on system time.

&#x20;  \* They eliminate issues like clock drift or inconsistent time across nodes.



3\. \*\*Simple Implementation\*\*



&#x20;  \* Each record stores a small JSON structure:



&#x20;    ```json

&#x20;    {"us": 2, "eu": 1, "apac": 0}

&#x20;    ```

&#x20;  \* Easy to update, compare, and merge.



4\. \*\*Deterministic Behavior\*\*



&#x20;  \* Every node independently arrives at the same conclusion about conflicts.



\---



\## ⚠️ Limitations of Vector Clocks



\* They \*\*only detect conflicts\*\*, not resolve them automatically.

\* Additional logic (like LWW) is required for resolution.

\* Vector size grows with number of nodes.

\* Not ideal for complex data structures.



\---



\## 🔄 Why Not CRDTs?



CRDTs (Conflict-free Replicated Data Types) are designed to \*\*automatically resolve conflicts\*\* without coordination.



However, they were not chosen for this project due to:



1\. \*\*Overhead for Simple Use Case\*\*



&#x20;  \* Our system only updates simple fields like price.

&#x20;  \* Using CRDTs would add unnecessary complexity.



2\. \*\*Business Logic Simplicity\*\*



&#x20;  \* LWW (Last-Write-Wins) is sufficient and easier to implement.

&#x20;  \* No need for advanced merge strategies.



3\. \*\*Learning Objective\*\*



&#x20;  \* The goal of this project is to understand:



&#x20;    \* Conflict detection

&#x20;    \* Distributed system behavior

&#x20;  \* Vector clocks provide better conceptual clarity.



\---



\## 🔄 When CRDTs Would Be Better



CRDTs would be a better choice in the following scenarios:



1\. \*\*Complex Data Types\*\*



&#x20;  \* Counters (e.g., likes, views)

&#x20;  \* Lists (e.g., comments, messages)

&#x20;  \* Sets (e.g., tags, categories)



2\. \*\*Frequent Concurrent Updates\*\*



&#x20;  \* Systems with high write concurrency

&#x20;  \* Real-time collaborative applications



3\. \*\*Automatic Conflict Resolution Needed\*\*



&#x20;  \* No manual resolution logic required

&#x20;  \* System must always merge data safely



4\. \*\*Offline-first Applications\*\*



&#x20;  \* Mobile apps syncing data after disconnection



\---



\## ⚖️ Trade-off Summary



| Feature             | Vector Clocks | CRDTs                      |

| ------------------- | ------------- | -------------------------- |

| Conflict Detection  | ✅ Yes         | ✅ Yes                      |

| Conflict Resolution | ❌ Manual      | ✅ Automatic                |

| Complexity          | Low           | High                       |

| Flexibility         | Medium        | High                       |

| Best Use Case       | Simple data   | Complex collaborative data |



\---



\## ✅ Final Decision



Vector clocks were chosen because they:



\* Provide clear conflict detection

\* Are easy to implement and understand

\* Fit well with the LWW strategy

\* Match the simplicity of the product catalog use case



CRDTs, while powerful, were not necessary for this level of complexity.



\---



\## 📌 Conclusion



This design balances \*\*simplicity and correctness\*\* by:



\* Using vector clocks for accurate conflict detection

\* Applying deterministic LWW logic for resolution



It reflects a practical approach used in real-world distributed systems where trade-offs between complexity and functionality must be carefully considered.



\---



