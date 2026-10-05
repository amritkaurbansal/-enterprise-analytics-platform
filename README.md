# 📊 Real-Time Enterprise Transaction Analytics Platform

A high-performance, event-driven streaming data architecture built to simulate, ingest, store, and visually track live corporate transaction data as it happens. This framework eliminates data reporting latency by transforming raw events into immediate, actionable dashboard metrics.

---

## 🛠️ Tech Stack & Architecture

- **Language:** Python 3.14 (Core system loops, pipelines, and aggregation backend)
- **Database Engine:** SQLite (Embedded, lightning-fast relational storage layer)
- **API Framework:** FastAPI (Asynchronous framework configured to serve analytics JSON endpoints)
- **Frontend Layer:** Streamlit (Dynamic web engine powered by Plotly & Pandas for 2-second real-time dashboard updates)

---

## 📂 System Core Modules

1. **Automated Data Ingestor (`pipelines/ingest_data.py`)**
   - Continuously simulates streaming business transactions from multiple checkout lines (Web Store, Mobile App, Retail POS, Wholesale API).
   - Dynamically signs distinct transaction IDs, random transactional values, and handles synthetic failure metrics with distributed gateway error tracking logs.

2. **Persistent Storage Layer (`enterprise_analytics.db`)**
   - Receives massive transaction datasets natively on your drive.
   - Structured relational schemas process math aggregates reliably under sudden traffic surges.

3. **Visual Live Interface (`dashboard.py`)**
   - Performs asynchronous aggregation loops (`COUNT(*)`, `SUM(amount)`) every 2 seconds.
   - Automatically renders real-time financial totals, interactive success distribution charts, and a running live log ledger tracking operational telemetry.

---

## 🚀 Local Installation & Running Guide

### 1. Initialize and install dependencies
```bash
pip install -r requirements.txt
pip install streamlit requests pandas plotly
```

### 2. Boot up the Automated Data Ingestor
```bash
python pipelines/ingest_data.py
```
*(Keep this window open to generate live transaction traffic)*

### 3. Spin up the Visual Analytics UI
```bash
streamlit run dashboard.py
```
---
