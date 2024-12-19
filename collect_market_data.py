import yfinance as yf
import sqlite3
import time
import yaml
from datetime import datetime

# SQLite database setup
def setup_database(tickers):
    conn = sqlite3.connect("market_data.db")
    cursor = conn.cursor()

    print(type(tickers), tickers)
    for row in tickers:
        for table_name, _ in row.items():
            safe_table_name = table_name.replace("-", "_").replace("=", "_")
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS "{safe_table_name}" (
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
def fetch_and_store_data(tickers):
    conn = sqlite3.connect("market_data.db")
    cursor = conn.cursor()

    for row in tickers:
        for table_name, ticker in row.items():
            safe_table_name = table_name.replace("-", "_").replace("=", "_")
            yf_ticker = yf.Ticker(ticker)
            data = yf_ticker.history(interval="1m", period="1h")

            for timestamp, row in data.iterrows():
                timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                open_price = row['Open']
                high_price = row['High']
                low_price = row['Low']
                close_price = row['Close']
                volume = row['Volume']

                try:
                    cursor.execute(f'''
                        INSERT OR IGNORE INTO "{safe_table_name}" (timestamp, open, high, low, close, volume)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (timestamp_str, open_price, high_price, low_price, close_price, volume))
                except sqlite3.Error as e:
                    print(f"Error inserting data for {ticker}: {e}")

    conn.commit()
    conn.close()

# Load configuration from YAML file
def load_config(config_file="config.yaml"):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config.get("tickers", {})

# Main function to schedule data collection
def main():
    tickers = load_config()
    if not tickers:
        print("No tickers found in the configuration file.")
        return

    setup_database(tickers)
    while True:
        fetch_and_store_data(tickers)
        print(f"Data fetched and stored at {datetime.now()}.")
        time.sleep(60)  # Wait for 1 minute

if __name__ == "__main__":
    main()
