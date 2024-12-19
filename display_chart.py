import sqlite3
import pandas as pd
import plotly.graph_objects as go

# Read data from SQLite database
def read_data(ticker):
    conn = sqlite3.connect("market_data.db")
    table_name = ticker.replace("-", "_").replace("=", "_")
    query = f"SELECT * FROM \"{table_name}\" ORDER BY timestamp"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# Plot candlestick chart with volume
def plot_candlestick_chart(df, ticker):
    fig = go.Figure()

    # Add candlestick chart
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name="Candlestick"
    ))

    # Add volume bar chart
    fig.add_trace(go.Bar(
        x=df['timestamp'],
        y=df['volume'],
        name="Volume",
        marker_color='rgba(128, 128, 128, 0.5)',
        yaxis="y2"
    ))

    # Update layout for dual y-axes
    fig.update_layout(
        title=f"{ticker} Candlestick Chart with Volume",
        xaxis_title="Timestamp",
        yaxis_title="Price",
        yaxis2=dict(
            title="Volume",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.show()

# Main function
def main():
    ticker = input("Enter the ticker symbol to plot (e.g., USD_Index, BTC_USD in config.yaml file): ").strip()
    df = read_data(ticker)
    if not df.empty:
        plot_candlestick_chart(df, ticker)
    else:
        print(f"No data available in the database for ticker: {ticker}.")

if __name__ == "__main__":
    main()
