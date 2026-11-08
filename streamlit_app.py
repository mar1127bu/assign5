
import yfinance as yf
import streamlit as st
import pandas as pd

# App title
st.title("MSFT Sharpe Ratio")

# Define ticker and risk-free rate
ticker = "MSFT"
rf_monthly = 0.0025

# Download stock data
st.write("Connecting to Yahoo Finance...")

try:
    with st.spinner("Downloading MSFT stock data..."):
        data = yf.download(
            ticker,
            period="5y",
            interval="1mo",
            progress=False,
            timeout=15,
            threads=False
        )

    st.write("Download complete!")

except Exception as e:
    st.error(f"Unable to download stock data: {e}")
    st.stop()

# Check if data was downloaded
if data.empty:
    st.error("No stock data was returned by Yahoo Finance.")
    st.stop()

# Extract closing prices
close_prices = data["Close"].squeeze()

# Calculate monthly returns
monthly_returns = close_prices.pct_change().dropna()

if monthly_returns.empty:
    st.error("Not enough stock data to calculate returns.")
    st.stop()

# Calculate excess returns
excess_returns = monthly_returns - rf_monthly

# Calculate average excess return and standard deviation
mean_excess_return = excess_returns.mean()
std_dev_return = monthly_returns.std()

# Calculate monthly Sharpe Ratio
if std_dev_return != 0:
    monthly_sharpe_ratio = mean_excess_return / std_dev_return

    st.write(f"Ticker: {ticker}")
    st.metric(
        "Monthly Sharpe Ratio",
        f"{monthly_sharpe_ratio:.3f}"
    )

    st.write("Monthly stock returns:")
    st.line_chart(monthly_returns)

else:
    st.error("Standard deviation is zero; Sharpe Ratio cannot be calculated.")

