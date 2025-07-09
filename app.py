import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# --------- Data & Indicator Functions ---------

@st.cache_data
def load_data(ticker, period="1y"):
    df = yf.download(ticker, period=period, interval="1d")
    df.dropna(inplace=True)
    return df

def compute_rsi(prices, window=14):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# --------- Streamlit App ---------

def main():
    st.title("📈 Bitcoin RSI Dashboard")

    # --- Sidebar controls ---
    st.sidebar.header("Settings")
    rsi_window = st.sidebar.slider("RSI Window", 2, 30, 14)
    period = st.sidebar.selectbox("Price History", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

    # --- Load data ---
    df = load_data("BTC-USD", period)
    df["RSI"] = compute_rsi(df["Close"], window=rsi_window)

    # --- Display charts ---
    st.subheader("Bitcoin Price")
    st.line_chart(df["Close"])

    st.subheader(f"RSI (window={rsi_window})")
    st.line_chart(df["RSI"])

    # --- Signal example ---
    st.subheader("📍 RSI Regime Signal")
    if df["RSI"].iloc[-1] < 30:
        st.success("RSI indicates **Oversold** — possible buy signal ✅")
    elif df["RSI"].iloc[-1] > 70:
        st.warning("RSI indicates **Overbought** — caution advised ⚠️")
    else:
        st.info("RSI is in neutral range.")

if __name__ == "__main__":
    main()
