import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# Streamlit Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Yahoo Finance Stock Viewer",
    page_icon="📈",
    layout="wide"
)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("📈 Yahoo Finance Stock Viewer")
st.write("Fetch historical stock prices from Yahoo Finance and visualize the closing price.")

# -------------------------------------------------
# User Input
# -------------------------------------------------
ticker = st.text_input(
    "Enter Stock Symbol",
    value="AAPL",
    help="Examples: AAPL, MSFT, TSLA, RELIANCE.NS, TCS.NS, ^NSEI"
).strip().upper()

# -------------------------------------------------
# Period Selection
# -------------------------------------------------
period_options = {
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y",
    "10 Years": "10y",
    "Maximum": "max"
}

selected_period = st.selectbox(
    "Select Time Period",
    list(period_options.keys())
)

# -------------------------------------------------
# Interval Selection
# -------------------------------------------------
interval_options = {
    "Daily": "1d",
    "Weekly": "1wk",
    "Monthly": "1mo"
}

selected_interval = st.selectbox(
    "Select Data Interval",
    list(interval_options.keys())
)

# -------------------------------------------------
# Fetch Data
# -------------------------------------------------
if st.button("Fetch Data", type="primary"):

    if ticker == "":
        st.warning("Please enter a stock symbol.")
        st.stop()

    with st.spinner("Downloading data from Yahoo Finance..."):

        try:
            data = yf.download(
                tickers=ticker,
                period=period_options[selected_period],
                interval=interval_options[selected_interval],
                auto_adjust=True,
                progress=False,
                threads=False
            )

            # Check if data exists
            if data.empty:
                st.error("No data found. Please check the ticker symbol.")
                st.stop()

            # Handle MultiIndex columns (newer yfinance versions)
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            # Ensure Close column exists
            if "Close" not in data.columns:
                st.error("Closing price data is unavailable.")
                st.stop()

            close_prices = data["Close"]

            # -------------------------------------------------
            # Display Line Chart
            # -------------------------------------------------
            st.subheader(f"{ticker} Closing Price")

            fig, ax = plt.subplots(figsize=(12, 5))

            ax.plot(
                close_prices.index,
                close_prices.values,
                linewidth=2
            )

            ax.set_title(f"{ticker} Closing Price")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.grid(True)

            st.pyplot(fig, clear_figure=True)

            # -------------------------------------------------
            # Display Data
            # -------------------------------------------------
            st.subheader("Historical Data")

            st.dataframe(
                data.round(2),
                use_container_width=True
            )

            # -------------------------------------------------
            # Download CSV
            # -------------------------------------------------
            csv = data.to_csv().encode("utf-8")

            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{ticker}_{period_options[selected_period]}.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"An error occurred:\n\n{e}")
