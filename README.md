# Multi-Master Data Replication System

## 📌 Overview

This project simulates a **three-region multi-master replication system** for a product catalog.
Each region (US, EU, APAC) maintains its own database and accepts independent writes.

The system ensures **eventual consistency** across all regions using:

* Vector Clocks (for conflict detection)
* Last-Write-Wins (LWW) strategy (for conflict resolution)

---

## 🏗️ Architecture

* **db-us, db-eu, db-apac** → PostgreSQL databases (regional nodes)
* **Replication Service** → Python-based logic for syncing data
* **MinIO** → Object storage for snapshots
* **CLI Monitor** → Displays system metrics

---

## ⚙️ Tech Stack

* Python
* PostgreSQL
* Docker & Docker Compose
* MinIO (S3-compatible storage)
* psycopg2 (DB connection)
* boto3 (object storage)

---

## 🧠 Core Concepts

### 1. Multi-Master Replication

All nodes can accept writes independently.

### 2. Vector Clocks

Each record tracks updates from all nodes:

```json
{"us": 5, "eu": 3, "apac": 2}
```

### 3. Conflict Detection

* SUCCESSOR → accept update
* ANCESTOR → ignore update
* CONCURRENT → conflict

### 4. Conflict Resolution (LWW)

* Deterministic rule: higher node ID wins
* Merge clocks using max values

---

## 🚀 Setup Instructions

### 1. Clone Repository

```bash
git clone <repo-url>
cd multi-master-replication
```

### 2. Start Services

```bash
docker-compose up -d
```

### 3. Verify Containers

```bash
docker ps
```

---

## 🗄️ Database Schema

### product_catalog

* id (UUID)
* name
* price
* vector_clock (JSON)
* last_updated_by
* updated_at

### conflict_log

* product_id
* winning_version
* losing_version
* resolved_by_node

---

## 🔁 Replication Flow

1. Update happens in one region
2. Vector clock is incremented
3. Update is propagated to other nodes
4. Nodes compare vector clocks
5. Conflict resolved if needed

---

## 🧪 Testing

### Test Replication

```bash
python test_replication.py
```

### Test Conflict

```bash
python test_conflict.py
```

---

## 📊 Monitoring

Run:

```bash
python monitor.py
```

Displays:

* Region
* Replication Lag
* Conflict Rate

---

## 💾 Snapshot (MinIO)

Trigger snapshot:

```bash
python checkpoint.py
```

* Stored in: `database-snapshots` bucket
* Format: JSON file

---

## ⚠️ Known Issues

* Password authentication issues may occur due to Docker volume reuse

Fix:

```bash
docker-compose down -v
```

---

## 📄 Design Decision

Vector clocks were used because:

* They track causality between updates
* Help detect concurrent updates

CRDTs were not used because:

* This system uses simple overwrite logic (LWW)
* CRDTs are better for complex merge scenarios

---

## ✅ Features

* Multi-region simulation
* Conflict detection & resolution
* Eventual consistency
* CLI monitoring
* Snapshot backup

---

## 📌 Conclusion

This project demonstrates how distributed systems handle:

* Data replication
* Conflict resolution
* Fault tolerance

It reflects real-world systems used in global applications like e-commerce platforms.

---
