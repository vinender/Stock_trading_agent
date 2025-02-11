import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def get_stock_data(symbol, period='1mo'):
    """Fetch stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

def format_analysis(analysis):
    """Format AI analysis for better presentation"""
    sections = analysis.split('\n')
    formatted = ""
    
    for section in sections:
        if section.strip():
            if any(keyword in section.lower() for keyword in ['bullish', 'positive', 'upward']):
                formatted += f"🟢 {section}\n"
            elif any(keyword in section.lower() for keyword in ['bearish', 'negative', 'downward']):
                formatted += f"🔴 {section}\n"
            else:
                formatted += f"ℹ️ {section}\n"
    
    return formatted
