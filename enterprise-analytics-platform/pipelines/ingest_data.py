import sqlite3
import time
import random
import uuid

# Connects to a local SQLite database file instantly
conn = sqlite3.connect('enterprise_analytics.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS business_transactions (
    transaction_id TEXT PRIMARY KEY,
    channel TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT NOT NULL,
    error_code TEXT
)
''')
conn.commit()

CHANNELS = ['Web Store', 'Mobile App', 'Retail POS', 'Wholesale API']
STATUSES = ['SUCCESS', 'SUCCESS', 'SUCCESS', 'FAILED']  # 75% success rate
ERROR_CODES = ['ERR_TIMEOUT', 'ERR_INSUFFICIENT_FUNDS', 'ERR_CARD_DECLINED', 'ERR_GATEWAY_DOWN']

print("Starting Automated SQLite Ingestion Pipeline...")
print("Press Ctrl + C to stop at any time.\n")

try:
    while True:
        tx_id = f"TX-{str(uuid.uuid4())[:8].upper()}"
        channel = random.choice(CHANNELS)
        amount = round(random.uniform(5.00, 1200.00), 2)
        status = random.choice(STATUSES)
        error_code = random.choice(ERROR_CODES) if status == 'FAILED' else None

        cursor.execute('''
            INSERT INTO business_transactions (transaction_id, channel, amount, status, error_code)
            VALUES (?, ?, ?, ?, ?)
        ''', (tx_id, channel, amount, status, error_code))
        conn.commit()

        print(f"[✓] Ingested Transaction: {tx_id} | {channel} | ${amount} | {status}")
        time.sleep(2)  # Generates data every 2 seconds

except KeyboardInterrupt:
    print("\n[!] Pipeline stopped by user.")
finally:
      conn.close()