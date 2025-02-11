import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from stock_analyzer import StockAnalyzer
from ai_analyzer import AIAnalyzer
from utils import get_stock_data, format_analysis
from patterns import identify_patterns

st.set_page_config(page_title="Indian Stock Market Analysis", layout="wide")

def main():
    st.title("🚀 AI-Powered Indian Stock Market Analysis")
    
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
            st.header(f"Analysis for {stock}")
            
            # Get stock data
            df = get_stock_data(stock)
            
            if df is not None:
                # Create stock analyzer instance
                analyzer = StockAnalyzer(df)
                ai_analyzer = AIAnalyzer()

                # Display candlestick chart
                fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])
                
                fig.update_layout(title=f"{stock} Candlestick Chart",
                                xaxis_title="Date",
                                yaxis_title="Price")
                st.plotly_chart(fig)

                # Pattern Analysis
                patterns = identify_patterns(df)
                st.subheader("📊 Pattern Analysis")
                for pattern, description in patterns.items():
                    st.write(f"**{pattern}:** {description}")

                # AI Analysis
                st.subheader("🤖 AI Analysis")
                ai_analysis = ai_analyzer.analyze_stock(df)
                formatted_analysis = format_analysis(ai_analysis)
                st.write(formatted_analysis)

                # Performance Metrics
                st.subheader("📈 Performance Metrics")
                metrics = analyzer.calculate_metrics()
                col1, col2, col3 = st.columns(3)
                col1.metric("RSI", f"{metrics['rsi']:.2f}")
                col2.metric("MACD", f"{metrics['macd']:.2f}")
                col3.metric("Volume Change", f"{metrics['volume_change']:.2f}%")

if __name__ == "__main__":
    main()
