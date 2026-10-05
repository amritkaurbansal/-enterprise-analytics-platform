import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os
import time

st.set_page_config(page_title="Enterprise Analytics Dashboard", layout="wide")

st.title("📊 Live Enterprise Analytics Dashboard")
st.write("Real-time business transactions engine powered by FastAPI & SQLite")

# Locate the live database file directly
DB_PATH = os.path.join(os.path.dirname(__file__), "pipelines", "enterprise_analytics.db")
if not os.path.exists(DB_PATH):
    DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pipelines", "enterprise_analytics.db")

metrics_placeholder = st.empty()

while True:
    try:
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # 1. Fetch overall metrics
            cursor.execute("SELECT COUNT(*), SUM(amount) FROM business_transactions")
            total_count, total_revenue = cursor.fetchone()
            
            # 2. Fetch success vs failure rates
            cursor.execute("SELECT status, COUNT(*) FROM business_transactions GROUP BY status")
            status_data = dict(cursor.fetchall())
            
            # 3. Fetch channel metrics cleanly
            cursor.execute("SELECT channel, COUNT(*), SUM(amount) FROM business_transactions GROUP BY channel")
            channel_rows = cursor.fetchall()
            
            # 4. Fetch the 10 latest transaction rows for the data table
            cursor.execute("SELECT transaction_id, channel, amount, status, error_code FROM business_transactions ORDER BY rowid DESC LIMIT 10")
            recent_tx_rows = cursor.fetchall()
            
            conn.close()

            with metrics_placeholder.container():
                # Top Row: Key Metrics
                col1, col2 = st.columns(2)
                col1.metric("Total Transactions", f"{total_count:,}" if total_count else "0")
                col2.metric("Total Revenue", f"${total_revenue:,.2f}" if total_revenue else "$0.00")
                
                # Middle Row: Visual Charts
                col3, col4 = st.columns(2)
                
                # Pie Chart
                if status_data:
                    status_df = pd.DataFrame(list(status_data.items()), columns=['Status', 'Count'])
                    fig_status = px.pie(status_df, values='Count', names='Status', title="Transaction Success vs Failure",
                                        color_discrete_map={'SUCCESS': '#2ecc71', 'FAILED': '#e74c3c'})
                    col3.plotly_chart(fig_status, use_container_width=True)
                
                # Fixed Clean Bar Chart
                if channel_rows:
                    channel_data = [{"Channel": r[0], "Transactions": r[1], "Revenue": round(r[2], 2)} for r in channel_rows]
                    channel_df = pd.DataFrame(channel_data)
                    fig_channel = px.bar(channel_df, x='Channel', y='Revenue', title="Revenue Breakdown by Channel", text_auto='$.2s')
                    col4.plotly_chart(fig_channel, use_container_width=True)
                
                # Bottom Section: Live Log Feed
                st.subheader("📋 Recent Transaction Logs (Live Feed)")
                if recent_tx_rows:
                    logs_df = pd.DataFrame(recent_tx_rows, columns=["Transaction ID", "Channel", "Amount ($)", "Status", "Error Code"])
                    st.dataframe(logs_df, use_container_width=True, hide_index=True)
                    
        else:
            with metrics_placeholder.container():
                st.warning("Looking for the database file... Make sure your ingestion pipeline is running.")
            
    except Exception as e:
        with metrics_placeholder.container():
            st.error(f"Dashboard Error: {str(e)}")
        
    time.sleep(2)