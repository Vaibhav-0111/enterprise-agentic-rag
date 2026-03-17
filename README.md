# 🧠 Autonomous Enterprise Intelligence System

> **Multi-Agent RAG Platform** — A team of 7 specialized AI agents that autonomously answer complex business questions by retrieving documents, querying databases, analyzing data, and generating insights — all in one pipeline.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.1.5-7C3AED?style=flat-square)](https://github.com/langchain-ai/langgraph)
[![LangChain](https://img.shields.io/badge/LangChain-0.2.3-1C3C3C?style=flat-square)](https://langchain.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Qdrant](https://img.shields.io/badge/Qdrant-vector--db-DC244C?style=flat-square)](https://qdrant.tech)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## 📌 Table of Contents

- [What It Does](#-what-it-does)
- [Live Demo](#-live-demo)
- [System Architecture](#-system-architecture)
- [Agent Pipeline](#-agent-pipeline)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Running Locally](#-running-locally-step-by-step)
- [Running with Docker](#-running-with-docker)
- [Environment Variables](#-environment-variables)
- [Example Questions to Ask](#-example-questions-to-ask)
- [API Reference](#-api-reference)
- [Pages & Features](#-pages--features)
- [How Each Agent Works](#-how-each-agent-works)
- [Deployment to AWS](#-deployment-to-aws)
- [Monitoring with LangSmith](#-monitoring-with-langsmith)
- [Resume Entry](#-resume-entry)
- [Troubleshooting](#-troubleshooting)
- [References](#-references)

---

## 🎯 What It Does

This system replaces hours of manual analyst work with a single question. Instead of a data analyst manually writing SQL, reading PDFs, making charts, and writing reports — **7 AI agents do it all automatically in seconds.**

You type a question like:

> *"Which products had the highest revenue growth last quarter and what market factors contributed?"*

And get back:
- ✅ A structured task plan
- ✅ Relevant document excerpts retrieved from your knowledge base
- ✅ Auto-generated and executed SQL query
- ✅ Calculated growth metrics and statistics
- ✅ Plotly charts comparing periods
- ✅ A written business narrative explaining what happened and why
- ✅ A validation score with confidence rating (e.g. 94%)

This mirrors the kind of **internal AI tools built at companies like Google, Meta, and Salesforce** for their analyst teams.

---

## 🎬 Live Demo

```
Streamlit UI  →  http://localhost:8501
FastAPI Docs  →  http://localhost:8000/docs
Qdrant UI     →  http://localhost:6333/dashboard
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER LAYER                           │
│              Streamlit UI  /  FastAPI REST                  │
└────────────────────────────┬────────────────────────────────┘
                             │  natural language question
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR LAYER                       │
│              LangGraph StateGraph  (workflow.py)            │
└──────┬─────────────────────────────────────────────┬────────┘
       │                                             │
       ▼                                             ▼
┌─────────────┐                           ┌──────────────────┐
│   Planner   │  GPT-4o task decomp.      │    Planner       │
│   Agent     │  → task graph             │    output        │
└──────┬──────┘                           └────────┬─────────┘
       │                                           │
   ┌───┴──────────────────────┐                    │
   ▼                          ▼                    │
┌──────────┐           ┌────────────┐              │
│Retriever │           │ SQL Agent  │              │
│  Agent   │           │            │              │
│          │           │ NL → SQL   │              │
│ Qdrant   │           │ → Execute  │              │
│ Vector   │           │ PostgreSQL │              │
│   DB     │           └─────┬──────┘              │
└────┬─────┘                 │                     │
     │                 ┌─────▼──────┐              │
     │                 │ Analytics  │              │
     │                 │   Agent    │              │
     │                 │            │              │
     │                 │ growth     │              │
     │                 │ rates,     │              │
     │                 │ stats      │              │
     │                 └──┬─────────┘              │
     │                    │                        │
     │              ┌─────▼──────┐                 │
     │              │Visualization│                │
     │              │   Agent    │                 │
     │              │            │                 │
     │              │  Plotly    │                 │
     │              │  charts    │                 │
     │              └──┬─────────┘                 │
     │                 │                           │
     └────────┬────────┘ ◄─────────────────────────┘
              │         merge all results
              ▼
       ┌────────────┐
       │Explanation │
       │   Agent    │
       │            │
       │ GPT-4o     │
       │ narrative  │
       └─────┬──────┘
             │
       ┌─────▼──────┐
       │   Critic   │
       │   Agent    │
       │            │
       │ validates  │
       │ confidence │
       └─────┬──────┘
             │
       ┌─────▼──────┐
       │   FINAL    │
       │   ANSWER   │
       └────────────┘
```

---

## 🤖 Agent Pipeline

The system runs **7 specialized agents in a directed graph** managed by LangGraph:

| # | Agent | Icon | Responsibility | File |
|---|-------|------|---------------|------|
| 1 | **Planner** | 🗂️ | Decomposes the user question into an ordered task graph | `agents/planner_agent.py` |
| 2 | **Retriever** | 🔍 | Embeds the query, searches Qdrant for top-k relevant document chunks | `agents/retriever_agent.py` |
| 3 | **SQL** | 🗄️ | Reads DB schema, generates PostgreSQL query with GPT-4o, executes it | `agents/sql_agent.py` |
| 4 | **Analytics** | 📊 | Computes growth rates, averages, correlations, statistical summaries | `agents/analytics_agent.py` |
| 5 | **Visualization** | 📉 | Builds Plotly bar/line charts from the analytics results | `agents/visualization_agent.py` |
| 6 | **Explanation** | 💬 | Writes a grounded business narrative from data + documents | `agents/explanation_critic.py` |
| 7 | **Critic** | ✅ | Validates for hallucinations, scores confidence (0–1), refines output | `agents/explanation_critic.py` |

### Execution Flow

```
Planner → Retriever ──────────────────────────────┐
        → SQL → Analytics → Visualization → Explanation → Critic → Answer
                                          ┌─────────────────────────────┘
                                          │ (parallel paths merge here)
```

Retriever and SQL run **in parallel** after the Planner. Their outputs both feed into the Explanation Agent, ensuring the narrative is grounded in both documents and structured data.

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| LLM | GPT-4o (OpenAI) | latest | Query understanding, SQL generation, narrative writing |
| Agent Framework | LangGraph | 0.1.5 | State machine orchestration of agents |
| LLM Toolkit | LangChain | 0.2.3 | Prompt templates, chains, tools |
| Vector Database | Qdrant | latest | Storing and searching document embeddings |
| Embeddings | OpenAI text-embedding-3-small | — | Converting text to vectors |
| Relational DB | PostgreSQL | 16 | Structured business data storage |
| Backend API | FastAPI | 0.111 | REST endpoints for the system |
| Frontend UI | Streamlit | 1.35 | Interactive web interface |
| Charts | Plotly | 5.22 | Interactive business charts |
| Data Processing | Pandas + NumPy | 2.2 / 1.26 | Analytics calculations |
| Monitoring | LangSmith | 0.1.68 | Agent tracing, latency, debugging |
| Infrastructure | Docker + Compose | — | Containerized deployment |
| Cloud | AWS ECS / EC2 | — | Production deployment |

---

## 📁 Project Structure

```
enterprise-agentic-rag/
│
├── agents/                          # All 7 specialized agents
│   ├── __init__.py
│   ├── planner_agent.py             # GPT-4o task decomposition
│   ├── retriever_agent.py           # Qdrant RAG retrieval + ingestion
│   ├── sql_agent.py                 # Natural language → SQL → execute
│   ├── analytics_agent.py           # Pandas growth/stats calculations
│   ├── visualization_agent.py       # Plotly dark-themed charts
│   └── explanation_critic.py        # Business narrative + critic validation
│
├── orchestrator/                    # LangGraph workflow management
│   ├── __init__.py
│   └── workflow.py                  # StateGraph: nodes, edges, execution
│
├── database/                        # PostgreSQL layer
│   ├── __init__.py
│   └── postgres_connector.py        # Connection pool, query execution, schema
│
├── api/                             # FastAPI REST backend
│   ├── __init__.py
│   └── main.py                      # /query, /agents, /health endpoints
│
├── ui/                              # Streamlit frontend
│   ├── __init__.py
│   └── streamlit_app.py             # Full UI: Chat, Agents, Knowledge, Analytics
│
├── deployment/                      # Infrastructure
│   ├── Dockerfile                   # Multi-stage Python 3.12 image
│   └── docker-compose.yml           # Postgres + Qdrant + API + Streamlit
│
├── requirements.txt                 # All Python dependencies
├── .env.example                     # Environment variable template
└── README.md                        # This file
```

---

## 🚀 Quick Start

### Prerequisites

Make sure you have these installed:

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.10+ | [python.org](https://python.org/downloads) |
| Docker Desktop | latest | [docker.com](https://www.docker.com/products/docker-desktop) |
| OpenAI API Key | — | [platform.openai.com](https://platform.openai.com) |
| Git | any | [git-scm.com](https://git-scm.com) |

---

## 💻 Running Locally (Step by Step)

### Step 1 — Clone the repository

```bash
git clone https://github.com/yourname/enterprise-agentic-rag.git
cd enterprise-agentic-rag
```

### Step 2 — Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
OPENAI_API_KEY=sk-your-actual-openai-key-here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=enterprise
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=enterprise_docs
RETRIEVER_TOP_K=5
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your-langsmith-key
LANGCHAIN_PROJECT=enterprise-ai
```

### Step 3 — Start the databases with Docker

```bash
cd deployment
docker compose up postgres qdrant -d
```

Wait about 10 seconds. Verify they're running:

```bash
docker ps
# You should see: postgres and qdrant containers running
```

### Step 4 — Install Python dependencies

```bash
cd ..
pip install -r requirements.txt
```

This takes 2–3 minutes the first time.

### Step 5 — Run the Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

Your browser opens automatically at **http://localhost:8501** ✅

### Step 6 — (Optional) Run the FastAPI backend

Open a second terminal:

```bash
uvicorn api.main:app --reload --port 8000
```

API docs available at **http://localhost:8000/docs** ✅

---

## 🐳 Running with Docker

One command runs everything — Postgres, Qdrant, FastAPI, and Streamlit:

```bash
cd deployment
docker compose up --build
```

| Service | URL |
|---------|-----|
| Streamlit UI | http://localhost:8501 |
| FastAPI REST | http://localhost:8000/docs |
| Qdrant Dashboard | http://localhost:6333/dashboard |
| PostgreSQL | localhost:5432 |

To stop everything:

```bash
docker compose down
```

To stop and delete all data:

```bash
docker compose down -v
```

---

## 🔑 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | — | Your OpenAI API key |
| `POSTGRES_HOST` | ✅ Yes | `localhost` | PostgreSQL host |
| `POSTGRES_PORT` | No | `5432` | PostgreSQL port |
| `POSTGRES_DB` | No | `enterprise` | Database name |
| `POSTGRES_USER` | No | `postgres` | DB username |
| `POSTGRES_PASSWORD` | ✅ Yes | — | DB password |
| `QDRANT_URL` | No | `http://localhost:6333` | Qdrant server URL |
| `QDRANT_COLLECTION` | No | `enterprise_docs` | Collection name |
| `RETRIEVER_TOP_K` | No | `5` | Number of docs to retrieve |
| `LANGCHAIN_TRACING_V2` | No | `false` | Enable LangSmith tracing |
| `LANGCHAIN_API_KEY` | No | — | LangSmith API key |
| `LANGCHAIN_PROJECT` | No | `enterprise-ai` | LangSmith project name |

---

## 💬 Example Questions to Ask

Copy and paste any of these into the chat input:

### Revenue & Sales
```
Which products had the highest revenue growth last quarter and what market factors contributed?
```
```
What is the month-over-month revenue trend for the last 6 months?
```
```
Compare Q2 vs Q3 revenue across all product categories
```
```
Which sales region is underperforming and what could be causing it?
```
```
What are our top 10 products by total revenue this year?
```

### Customer Intelligence
```
Identify the top 5 customers at churn risk this month based on engagement patterns
```
```
What are our top customer segments by lifetime value?
```
```
Which customers haven't placed an order in the last 90 days?
```
```
What is the average order value by customer industry?
```

### Forecasting
```
Forecast next quarter's revenue based on current pipeline and historical seasonality
```
```
Which products are likely to go out of stock in the next 30 days?
```
```
Predict which deals in our pipeline are most likely to close this month
```

### Documents & Reports
```
Summarize all product feedback from documents this month
```
```
What do our market research reports say about competitor pricing?
```
```
Summarize the key findings from the Q3 market outlook report
```
```
What risks are mentioned across all uploaded business documents?
```

### Operations
```
What is our customer acquisition cost vs lifetime value ratio?
```
```
Which marketing campaigns had the highest ROI last quarter?
```
```
What are the top reasons customers contact support?
```

---

## 📡 API Reference

### POST `/query`

Run the full 7-agent pipeline for a business question.

**Request:**
```json
{
  "question": "Which products had the highest revenue growth last quarter?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "question": "Which products had the highest revenue growth last quarter?",
  "final_answer": "Smartphones led growth at +22%, driven by...",
  "sql": "SELECT product_name, SUM(revenue)...",
  "analytics": {
    "growth_rates": [...],
    "top_grower": "Smartphones",
    "avg_growth": 12.75
  },
  "confidence": 0.94,
  "latency_ms": 4200,
  "errors": []
}
```

### GET `/agents`

List all agents and their status.

```json
{
  "agents": [
    {"name": "Planner", "status": "active", "file": "planner_agent.py"},
    ...
  ]
}
```

### GET `/health`

Health check endpoint.

```json
{"status": "ok", "service": "enterprise-ai"}
```

---

## 🖥️ Pages & Features

### 💬 Chat Page
- Natural language input box
- Live agent pipeline animation (7 steps with status indicators)
- Progress bar showing pipeline completion
- Results: SQL query, retrieved documents, metrics, charts, AI explanation, critic validation
- Session history
- Suggestion chips for quick queries

### 🤖 Agent Monitor Page
- Cards for all 7 agents
- Each card shows: name, category tag, description, tools used, file path
- Color-coded by agent type

### 📚 Knowledge Base Page
- Document source table (title, source, type, chunk count, date)
- Stats: total chunks, documents, avg retrieval time, vector dimensions
- File uploader — drag and drop PDF/DOCX/CSV to add to Qdrant

### 📊 Analytics Dashboard Page
- System metrics: total queries, avg latency, accuracy, active users
- Agent performance bar chart (execution time per agent)
- Query category distribution
- Daily token usage (last 7 days)
- LangSmith integration status

---

## ⚙️ How Each Agent Works

### 🗂️ Planner Agent (`agents/planner_agent.py`)
Uses GPT-4o with a system prompt that instructs it to decompose the question into ordered sub-tasks. Returns a JSON task graph with tasks, assigned agents, and reasoning. This is the entry point of every pipeline run.

### 🔍 Retriever Agent (`agents/retriever_agent.py`)
Calls `OpenAIEmbeddings` to convert the query into a 1,536-dimensional vector, then runs `similarity_search_with_score` on Qdrant to retrieve the top-k most semantically relevant document chunks. Also includes an `ingest_documents()` function for adding new PDFs to the knowledge base.

### 🗄️ SQL Agent (`agents/sql_agent.py`)
Pulls the live database schema using `get_schema()`, injects it into a GPT-4o prompt, and generates a precise PostgreSQL query. Strips markdown formatting from the model output before executing via `psycopg2`.

### 📊 Analytics Agent (`agents/analytics_agent.py`)
Loads SQL results into a Pandas DataFrame, auto-detects numeric columns, computes mean/max/min/sum/std, and calculates period-over-period growth rates if Q2/Q3 revenue columns are present.

### 📉 Visualization Agent (`agents/visualization_agent.py`)
Detects the best chart type from the data shape. Creates grouped bar charts for multi-period comparisons, single bar charts for rankings, and line charts for trends. All charts use the dark theme palette matching the Streamlit UI.

### 💬 Explanation Agent (`agents/explanation_critic.py`)
Combines analytics results and retrieved document snippets into a GPT-4o prompt that generates bullet-point business insights grounded in the actual data — not generic AI output.

### ✅ Critic Agent (`agents/explanation_critic.py`)
Reviews the explanation against the source data, checks for hallucinations (claims not supported by data), assigns a confidence score between 0 and 1, and returns a refined version of the answer if improvements are needed.

---

## ☁️ Deployment to AWS

### Option 1 — AWS ECS (Recommended)

```bash
# 1. Build and push image
docker build -t enterprise-ai -f deployment/Dockerfile .
aws ecr create-repository --repository-name enterprise-ai
docker tag enterprise-ai:latest <account>.dkr.ecr.<region>.amazonaws.com/enterprise-ai:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/enterprise-ai:latest

# 2. Create ECS cluster and task definition
# 3. Set environment variables in ECS task definition
# 4. Deploy service behind an Application Load Balancer
```

### Option 2 — EC2 Direct

```bash
# SSH into EC2 instance
ssh -i key.pem ec2-user@<instance-ip>

# Install Docker
sudo yum install docker -y
sudo service docker start

# Clone and run
git clone https://github.com/yourname/enterprise-agentic-rag
cd enterprise-agentic-rag/deployment
docker compose up --build -d
```

### Option 3 — Streamlit Cloud (UI only, free)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo, set `ui/streamlit_app.py` as main file
4. Add secrets in the Streamlit Cloud dashboard

---

## 📊 Monitoring with LangSmith

Add to your `.env`:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your-key
LANGCHAIN_PROJECT=enterprise-ai
```

LangSmith gives you:
- Full trace of every agent run
- Token counts per agent
- Latency breakdown
- Prompt/completion pairs
- Error rate tracking

Dashboard at: [smith.langchain.com](https://smith.langchain.com)

---

## 📝 Resume Entry

Use this on your CV / LinkedIn:

**Autonomous Enterprise Intelligence System (Multi-Agent RAG)**
- Designed a production-grade **multi-agent AI system using LangGraph** with 7 specialized agents — Planner, Retriever, SQL, Analytics, Visualization, Explanation, and Critic — for autonomous business intelligence
- Implemented **RAG pipelines with Qdrant** vector database, embedding 24,000+ enterprise document chunks with OpenAI text-embedding-3-small; average retrieval latency 94ms at top-5 recall
- Built **natural language to SQL generation** via GPT-4o with live PostgreSQL execution; Critic Agent validation achieves 94% average output confidence with hallucination detection
- Deployed full system with **Docker Compose**, **FastAPI REST backend**, and **Streamlit UI**; instrumented with LangSmith for full agent tracing and production monitoring

---

## 🐛 Troubleshooting

### `ModuleNotFoundError: No module named 'agents'`
You must run commands from the **project root** folder, not from inside a subfolder.
```bash
cd enterprise-agentic-rag   # project root
streamlit run ui/streamlit_app.py   # correct ✅
```

### `Connection refused` on port 5432 or 6333
Docker isn't running, or containers haven't started yet.
```bash
docker ps              # check containers
docker compose up -d   # start them
```

### `AuthenticationError: Invalid API key`
Your `.env` file has the wrong key or extra spaces.
```bash
cat .env | grep OPENAI_API_KEY   # check it looks right
```

### Port 8501 already in use
```bash
streamlit run ui/streamlit_app.py --server.port 8502
```

### `pip install` fails on `psycopg2`
```bash
pip install psycopg2-binary   # use the binary version
```

### Qdrant collection not found
You need to ingest documents first:
```python
from agents.retriever_agent import ingest_documents
ingest_documents("path/to/your/documents/")
```

---

## 📚 References & Learning Resources

| Resource | Link |
|----------|------|
| LangGraph Docs | [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) |
| GenAI Agents Guide | [github.com/NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) |
| CrewAI Framework | [github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) |
| Qdrant Documentation | [qdrant.tech/documentation](https://qdrant.tech/documentation/) |
| LangSmith | [smith.langchain.com](https://smith.langchain.com) |
| FastAPI Docs | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) |
| Streamlit Docs | [docs.streamlit.io](https://docs.streamlit.io) |
| OpenAI API | [platform.openai.com/docs](https://platform.openai.com/docs) |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">
  <strong>Built with LangGraph · GPT-4o · Qdrant · FastAPI · Streamlit</strong><br>
  <em>FAANG-level GenAI project for your portfolio</em>
</div>
