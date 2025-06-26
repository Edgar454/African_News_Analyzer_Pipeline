# 📰 Insight Africa

> *Stay informed without the noise.*

I haven’t had time to follow the news lately. While I generally find them overwhelming or even depressing, I still believe that staying informed is essential. That’s why I built **Insight Africa** — a platform that aggregates and summarizes news from a multitude of sources, helping users quickly grasp key stories and trends.

The platform combines **Data Engineering**, **Machine Learning**, and **Modern Web Development** to deliver insightful, digestible news updates through a clean and user-friendly interface.

---

## ⚙️ Project Overview

Insight Africa has three major components:

### 🔄 ETL Pipeline
- **Frequency:** Every 3 hours
- **Process:**  
  - An **Airflow DAG** scrapes data from multiple RSS feeds.
  - The raw data is ingested into **Kafka**.
  - A **Spark Streaming job** transforms the feed content and stores it in **PostgreSQL**.

### 🤖 Machine Learning
- A classification job assigns categories to each article (e.g., *Politics*, *Economy*, *Science/Tech*).
- Every week, batch **Spark jobs** are triggered to:
  - Generate a weekly summary
  - Perform **Topic Modeling**
  - Build a **Knowledge Graph**

### 🌐 API + React UI
- A **FastAPI backend** exposes RESTful endpoints to serve news data, summaries, metrics, and visualizations.
- A **React frontend** queries these endpoints and presents:
  - A daily and weekly summary of news
  - Topic tags and visualizations
  - An interactive knowledge graph
  - Search, filter, and category-based browsing

---

## 🗂 Architecture

<!-- Insert your architecture diagram here -->
![architecture](#)

---

## 🛠 Airflow DAGs

There are **three DAGs**, located in the `dags/` directory:

| DAG | Schedule | Purpose |
|-----|----------|---------|
| `scraping_dag` | Every 3 hours | Scrapes RSS feeds and triggers classification |
| `classification_dag` | Triggered by scraping | Classifies news using Spark |
| `weekly_summary_dag` | Weekly | Summarizes news, performs topic modeling, and builds a knowledge graph |

<!-- Insert DAG schema image -->
![dag-schema](#)

---

## 🚀 Local Installation (with Docker)

### 🔧 Requirements
Create a `.env` file in your root directory:

```env
# Airflow
AIRFLOW_UID=50000
AIRFLOW_IMAGE_NAME=apache/airflow:3.0.1
AIRFLOW_PROJ_DIR=.
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=admin
AIRFLOW_HOME=/opt/bitnami/airflow

# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka-1:9092

# Spark & App
MISTRAL_API_KEY=your_mistral_key_here
OUTPUT_DIR=/opt/output

# Postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=eded404
```

Get your **Mistral API key** here:  
[https://auth.mistral.ai/ui/login](https://auth.mistral.ai/ui/login)

---

### 🐳 Setup with Docker

1. **Initialize Airflow**
   ```bash
   docker-compose up airflow-init
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Create Kafka Topic**
   ```bash
   docker exec -it <KAFKA_CONTAINER_ID> bash
   kafka-topics.sh --create      --topic news_topic      --bootstrap-server localhost:9092      --partitions 2      --replication-factor 2
   ```

4. **Run Spark job for stream enhancement**
   ```bash
   docker exec -it <SPARK_CONTAINER_ID> bash
   spark-submit --master spark://spark-master:7077      --deploy-mode client      --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.kafka:kafka-clients:3.9.1      /opt/bitnami/spark/jobs/enhance_feeds.py
   ```

5. **Launch the frontend**
   The React app is served separately. After installing the frontend dependencies (`npm install`), you can run:
   ```bash
   npm run dev
   ```
   and access the app at [http://localhost:3000](http://localhost:3000)

---

## 🧠 API and Frontend Integration

The **FastAPI backend** serves all processed data through clean and intuitive REST endpoints:

| Endpoint | Purpose |
|----------|---------|
| `/news` | List all recent news |
| `/news/{id}` | Detailed view of a specific news item |
| `/weekly_summary` | Get the weekly AI-generated summary |
| `/topic_model` | Retrieve topic modeling HTML |
| `/network_metrics` | Get knowledge graph metrics |
| `/node_metrics` | Node-level centrality and influence |
| `/weekly_insights` | Weekly text-based insights |

These are consumed by the **React frontend**, which:
- Allows filtering by category, date, or source
- Includes a search bar for keyword-based filtering
- Shows dynamic graphs and tags from backend outputs
- Is designed with a clean and minimalist aesthetic (TailwindCSS + FontAwesome)

---

## ☁️ Cloud Deployment (Azure VM)

Due to the resource requirements (10GB disk, 2+ cores, 6GB+ RAM), local development may be limited.

To deploy on Azure or other VMs:
- Use `cloud.sh` for setup.
- Either run `docker.sh` or export `$AIRFLOW_HOME`, then go into the `airflow/` folder and follow the Docker Compose steps.

---

## 🧪 Demo

<!-- Insert demo GIF or video here -->
[Watch Demo](#)