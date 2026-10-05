from fastapi import FastAPI
import sqlite3
import os

app = FastAPI(title="Enterprise Analytics API")

# Path to the live SQLite file we just created
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "pipelines", "enterprise_analytics.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def read_root():
    return {"status": "online", "database": "SQLite Live Data Connected"}

@app.get("/api/v1/analytics/metrics")
def get_metrics():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Calculate overall metrics
        cursor.execute("SELECT COUNT(*), SUM(amount) FROM business_transactions")
        total_count, total_revenue = cursor.fetchone()
        
        # Calculate success vs failure rates
        cursor.execute("SELECT status, COUNT(*) FROM business_transactions GROUP BY status")
        status_data = dict(cursor.fetchall())
        
        # Calculate channel metrics
        cursor.execute("SELECT channel, COUNT(*), SUM(amount) FROM business_transactions GROUP BY channel")
        channels = {}
        for row in cursor.fetchall():
            channels[row[0]] = {"count": row[1], "revenue": round(row[2], 2) if row[2] else 0}
            
        conn.close()
        
        return {
            "total_transactions": total_count,
            "total_revenue": round(total_revenue, 2) if total_revenue else 0,
            "status_distribution": status_data,
            "channel_breakdown": channels
        }
    except Exception as e:
        return {"error": str(e)}