\# Multi-Master Data Replication System



\## 📌 Overview



This project simulates a \*\*three-region multi-master replication system\*\* for a product catalog.

Each region (US, EU, APAC) maintains its own database and accepts independent writes.



The system ensures \*\*eventual consistency\*\* across all regions using:



\* Vector Clocks (for conflict detection)

\* Last-Write-Wins (LWW) strategy (for conflict resolution)



\---



\## 🏗️ Architecture



\* \*\*db-us, db-eu, db-apac\*\* → PostgreSQL databases (regional nodes)

\* \*\*Replication Service\*\* → Python-based logic for syncing data

\* \*\*MinIO\*\* → Object storage for snapshots

\* \*\*CLI Monitor\*\* → Displays system metrics



\---



\## ⚙️ Tech Stack



\* Python

\* PostgreSQL

\* Docker \& Docker Compose

\* MinIO (S3-compatible storage)

\* psycopg2 (DB connection)

\* boto3 (object storage)



\---



\## 🧠 Core Concepts



\### 1. Multi-Master Replication



All nodes can accept writes independently.



\### 2. Vector Clocks



Each record tracks updates from all nodes:



```

{"us": 5, "eu": 3, "apac": 2}

```



\### 3. Conflict Detection



\* SUCCESSOR → accept update

\* ANCESTOR → ignore update

\* CONCURRENT → conflict



\### 4. Conflict Resolution (LWW)



\* Deterministic rule: higher node ID wins

\* Merge clocks using max values



\---



\## 🚀 Setup Instructions



\### 1. Clone Repository



```

git clone <repo-url>

cd multi-master-replication

```



\### 2. Start Services



```

docker-compose up -d

```



\### 3. Verify Containers



```

docker ps

```



\---



\## 🗄️ Database Schema



\### product\_catalog



\* id (UUID)

\* name

\* price

\* vector\_clock (JSON)

\* last\_updated\_by

\* updated\_at



\### conflict\_log



\* product\_id

\* winning\_version

\* losing\_version

\* resolved\_by\_node



\---



\## 🔁 Replication Flow



1\. Update happens in one region

2\. Vector clock is incremented

3\. Update is propagated to other nodes

4\. Nodes compare vector clocks

5\. Conflict resolved if needed



\---



\## 🧪 Testing



\### Test Replication



```

python test\_replication.py

```



\### Test Conflict



```

python test\_conflict.py

```



\---



\## 📊 Monitoring



Run:



```

python monitor.py

```



Displays:



\* Region

\* Replication Lag

\* Conflict Rate



\---



\## 💾 Snapshot (MinIO)



Trigger snapshot:



```

python checkpoint.py

```



\* Stored in: `database-snapshots` bucket

\* Format: JSON file



\---



\## ⚠️ Known Issues



\* Password authentication issues may occur due to Docker volume reuse

\* Fix by:



```

docker-compose down -v

```



\---



\## 📄 Design Decision



Vector clocks were used because:



\* They track causality between updates

\* Help detect concurrent updates



CRDTs were not used because:



\* This system uses simple overwrite logic (LWW)

\* CRDTs are better for complex merge scenarios



\---



\## ✅ Features



\* Multi-region simulation

\* Conflict detection \& resolution

\* Eventual consistency

\* CLI monitoring

\* Snapshot backup



\---



\## 📌 Conclusion



This project demonstrates how distributed systems handle:



\* Data replication

\* Conflict resolution

\* Fault tolerance



It reflects real-world systems used in global applications like e-commerce platforms.



\---



