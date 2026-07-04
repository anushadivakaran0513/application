import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Stock Price Viewer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Price Line Chart")

st.write("Fetch stock data directly from Yahoo Finance.")

ticker = st.text_input("Enter Stock Symbol", "AAPL")

period = st.selectbox(
    "Select Time Period",
    (
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "max"
    )
)

interval = st.selectbox(
    "Select Interval",
    (
        "1d",
        "1wk",
        "1mo"
    )
)

if st.button("Fetch Data"):

    try:
        data = yf.download(
            ticker,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=True
        )

        if data.empty:
            st.error("No data found.")
        else:

            st.success(f"Showing data for {ticker.upper()}")

            st.dataframe(data.tail())

            fig, ax = plt.subplots(figsize=(12,5))

            ax.plot(
                data.index,
                data["Close"],
                linewidth=2
            )

            ax.set_title(f"{ticker.upper()} Closing Price")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")

            ax.grid(True)

            st.pyplot(fig)

    except Exception as e:
        st.error(e)
