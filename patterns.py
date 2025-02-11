import numpy as np
import pandas as pd

def identify_patterns(df):
    """Identify candlestick patterns in the data"""
    patterns = {}
    
    # Doji pattern
    def is_doji(open_price, close_price, high, low):
        body = abs(open_price - close_price)
        upper_wick = high - max(open_price, close_price)
        lower_wick = min(open_price, close_price) - low
        return body <= (high - low) * 0.1

    # Hammer pattern
    def is_hammer(open_price, close_price, high, low):
        body = abs(open_price - close_price)
        upper_wick = high - max(open_price, close_price)
        lower_wick = min(open_price, close_price) - low
        return lower_wick > body * 2 and upper_wick <= body * 0.1

    # Check last candle
    last_candle = df.iloc[-1]
    if is_doji(last_candle['Open'], last_candle['Close'], 
               last_candle['High'], last_candle['Low']):
        patterns['Doji'] = 'Indicates market indecision, potential trend reversal'
        
    if is_hammer(last_candle['Open'], last_candle['Close'], 
                last_candle['High'], last_candle['Low']):
        patterns['Hammer'] = 'Potential bullish reversal pattern'

    # Trend patterns
    last_5_closes = df['Close'].tail(5)
    if all(last_5_closes.diff().dropna() > 0):
        patterns['Uptrend'] = 'Strong bullish momentum over last 5 days'
    elif all(last_5_closes.diff().dropna() < 0):
        patterns['Downtrend'] = 'Strong bearish momentum over last 5 days'

    return patterns
