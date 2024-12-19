import yfinance as yf

# Define the ticker for USD/JPY
ticker = "DX-Y.NYB"  # Yahoo Finance uses 'JPY=X' for USD/JPY currency pair

# Download 1 day of data
data = yf.download(ticker, period="1d", interval="1m")

# Display the data
print(data)
