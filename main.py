import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from stock_analyzer import StockAnalyzer
from ai_analyzer import AIAnalyzer
from utils import get_stock_data, format_analysis
from patterns import identify_patterns

# Configure Streamlit page
st.set_page_config(
    page_title="Indian Stock Market Analysis",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': 'AI-Powered Indian Stock Market Analysis Tool'
    }
)

def init_session_state():
    """Initialize session state variables"""
    if 'selected_stocks' not in st.session_state:
        st.session_state.selected_stocks = []

def main():
    try:
        st.title("🚀 AI-Powered Indian Stock Market Analysis")

        # Initialize session state
        init_session_state()

        # Sidebar
        st.sidebar.header("Configuration")
        selected_stocks = st.sidebar.multiselect(
            "Select Stocks",
            ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS"],
            default=["RELIANCE.NS"]
        )

        # Main content
        if selected_stocks:
            for stock in selected_stocks:
                try:
                    st.header(f"Analysis for {stock}")

                    # Get stock data with error handling
                    df = get_stock_data(stock)

                    if df is not None and not df.empty:
                        # Create stock analyzer instance
                        analyzer = StockAnalyzer(df)
                        ai_analyzer = AIAnalyzer()

                        # Display candlestick chart
                        fig = go.Figure(data=[go.Candlestick(x=df.index,
                            open=df['Open'],
                            high=df['High'],
                            low=df['Low'],
                            close=df['Close'])])

                        fig.update_layout(
                            title=f"{stock} Candlestick Chart",
                            xaxis_title="Date",
                            yaxis_title="Price",
                            template="plotly_white"
                        )
                        st.plotly_chart(fig, use_container_width=True)

                        # Pattern Analysis
                        with st.expander("📊 Pattern Analysis", expanded=True):
                            patterns = identify_patterns(df)
                            for pattern, description in patterns.items():
                                st.write(f"**{pattern}:** {description}")

                        # AI Analysis
                        with st.expander("🤖 AI Analysis", expanded=True):
                            ai_analysis = ai_analyzer.analyze_stock(df)
                            formatted_analysis = format_analysis(ai_analysis)
                            st.write(formatted_analysis)

                        # Performance Metrics
                        with st.expander("📈 Performance Metrics", expanded=True):
                            metrics = analyzer.calculate_metrics()
                            col1, col2, col3 = st.columns(3)
                            col1.metric("RSI", f"{metrics['rsi']:.2f}")
                            col2.metric("MACD", f"{metrics['macd']:.2f}")
                            col3.metric("Volume Change", f"{metrics['volume_change']:.2f}%")
                    else:
                        st.error(f"Unable to fetch data for {stock}. Please try again later.")
                except Exception as e:
                    st.error(f"Error analyzing {stock}: {str(e)}")
        else:
            st.info("Please select one or more stocks from the sidebar to begin analysis.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.info("Please try refreshing the page. If the issue persists, contact support.")

if __name__ == "__main__":
    main()