import yfinance as yf
import sqlite3
import time
from datetime import datetime

# SQLite database setup
def setup_database():
    conn = sqlite3.connect("usd_index_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usd_index (
            timestamp TEXT PRIMARY KEY,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Function to fetch and store data
def fetch_and_store_data():
    conn = sqlite3.connect("usd_index_data.db")
    cursor = conn.cursor()

    # Fetch data from Yahoo Finance
    ticker = yf.Ticker("DX-Y.NYB")
    data = ticker.history(interval="1m", period="1d")

    for timestamp, row in data.iterrows():
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        open_price = row['Open']
        high_price = row['High']
        low_price = row['Low']
        close_price = row['Close']
        volume = row['Volume']

        try:
            cursor.execute('''
                INSERT OR IGNORE INTO usd_index (timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (timestamp_str, open_price, high_price, low_price, close_price, volume))
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    conn.commit()
    conn.close()

# Main function to schedule data collection
def main():
    setup_database()
    while True:
        fetch_and_store_data()
        print(f"Data fetched and stored at {datetime.now()}.")
        time.sleep(60)  # Wait for 1 minute

if __name__ == "__main__":
    main()
