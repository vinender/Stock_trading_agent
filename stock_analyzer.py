import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD

class StockAnalyzer:
    def __init__(self, df):
        self.df = df

    def calculate_metrics(self):
        """Calculate various technical indicators"""
        # RSI
        rsi_indicator = RSIIndicator(close=self.df['Close'])
        rsi = rsi_indicator.rsi().iloc[-1]

        # MACD
        macd_indicator = MACD(close=self.df['Close'])
        macd = macd_indicator.macd().iloc[-1]

        # Volume Change
        volume_change = ((self.df['Volume'].iloc[-1] - self.df['Volume'].iloc[-2]) / 
                        self.df['Volume'].iloc[-2] * 100)

        return {
            'rsi': rsi,
            'macd': macd,
            'volume_change': volume_change
        }

    def analyze_trend(self):
        """Analyze current market trend"""
        last_price = self.df['Close'].iloc[-1]
        prev_price = self.df['Close'].iloc[-2]
        sma_20 = self.df['Close'].rolling(window=20).mean().iloc[-1]
        
        trend = "Bullish" if last_price > sma_20 else "Bearish"
        strength = abs((last_price - sma_20) / sma_20 * 100)
        
        return {
            'trend': trend,
            'strength': strength,
            'price_change': ((last_price - prev_price) / prev_price * 100)
        }
