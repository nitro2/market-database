import yfinance as yf
from datetime import datetime, timedelta

# Define the events with date and time
events = [
    ("2024-12-04", "08:15"),
    # ("2024-10-30", "07:15"),
    # ("2024-10-02", "07:15"),
    # ("2024-09-05", "07:15"),
    # ("2024-07-31", "07:15"),
    # ("2024-07-03", "07:15"),
    # ("2024-06-05", "07:15"),
    # ("2024-05-01", "07:15"),
    # ("2024-04-03", "07:15"),
    # ("2024-03-06", "08:15"),
    # ("2024-01-31", "08:15"),
    # ("2024-01-04", "08:15"),
]

# Initialize the ticker
ticker = "DX-Y.NYB"

# Function to fetch data for a specific event
def fetch_event_data(date_str, time_str):
    # Parse date and time
    # event_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    # start_time = event_time - timedelta(minutes=15)
    # end_time = event_time + timedelta(minutes=15)
    # print(start_time, end_time) 
    # Download data
    data = yf.download(
        ticker,
        # start=start_time.strftime("%Y-%m-%d %H:%M:%S"),
        # end=end_time.strftime("%Y-%m-%d %H:%M:%S"),
        start=date_str,
        end=date_str,
        interval="1m"
    )
    print(data)
    return data

# Fetch data for all events
all_event_data = {}
for date, time in events:
    print(f"Fetching data for {date} at {time}...")
    event_data = fetch_event_data(date, time)
    all_event_data[f"{date} {time}"] = event_data
    print(f"Data fetched for {date} {time}: {event_data.shape[0]} rows.")

# Example: Display the data for the first event
print(all_event_data[events[0][0] + " " + events[0][1]])
