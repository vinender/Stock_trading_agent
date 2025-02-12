import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import numpy as np
# from stock_analyzer import StockAnalyzer # Assuming stock_analyzer.py exists and is in the same directory or path
# from ai_analyzer import AIAnalyzer     # Assuming ai_analyzer.py exists and is in the same directory or path

st.set_page_config(page_title="Live Trading Analysis with Simulator", layout="wide")

def get_live_data(symbol, interval='1m', period='1d'):
    """Fetch live stock data."""
    stock = yf.Ticker(symbol)
    data = stock.history(interval=interval, period=period)
    return data

def calculate_max_drawdown(balance_history):
    """Calculate maximum drawdown from balance history."""
    peak = balance_history[0]
    max_dd = 0.0
    for balance in balance_history:
        if balance > peak:
            peak = balance
        dd = (peak - balance) / peak * 100
        if dd > max_dd:
            max_dd = dd
    return max_dd

class EnhancedSimulator:
    """Advanced paper-trading simulator with risk management and performance tracking."""
    def __init__(self, initial_balance=100000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = None        # "Long" or "Short"
        self.entry_price = None
        self.quantity = 0
        self.stop_loss = None
        self.target_price = None
        self.trade_log = []
        self.balance_history = [initial_balance]
        self.equity_history = []

    def open_position(self, position_type, price, time_stamp, stop_loss, target_price, risk_percent):
        """Open new position with risk management."""
        try:
            risk_amount = (risk_percent / 100) * self.balance
            if position_type == "Long":
                risk_per_share = price - stop_loss
                if risk_per_share <= 0:
                    raise ValueError("Invalid stop loss for Long position")
            elif position_type == "Short":
                risk_per_share = stop_loss - price
                if risk_per_share <= 0:
                    raise ValueError("Invalid stop loss for Short position")
            else:
                return

            quantity = int(risk_amount / risk_per_share)
            if quantity <= 0:
                raise ValueError("Invalid position size")

            # Check balance sufficiency
            if position_type == "Long":
                cost = price * quantity
                if cost > self.balance:
                    quantity = int(self.balance // price)
                    if quantity == 0:
                        raise ValueError("Insufficient funds for Long position")
                    cost = price * quantity
                self.balance -= cost
            else:  # Short
                proceeds = price * quantity
                margin_required = proceeds * 0.5  # Simplified margin requirement
                if margin_required > self.balance:
                    quantity = int((self.balance // (price * 0.5)))
                    if quantity == 0:
                        raise ValueError("Insufficient margin for Short position")
                self.balance += proceeds  # Credit short proceeds

            self.position = position_type
            self.entry_price = price
            self.quantity = quantity
            self.stop_loss = stop_loss
            self.target_price = target_price

            self.trade_log.append({
                "time": time_stamp,
                "action": f"Open {position_type}",
                "price": price,
                "quantity": quantity,
                "balance": self.balance,
                "stop_loss": stop_loss,
                "target_price": target_price
            })
            self.balance_history.append(self.balance)

        except Exception as e:
            st.error(f"Position opening failed: {str(e)}")

    def close_position(self, price, time_stamp, reason="Manual"):
        """Close current position and update balance."""
        if self.position is None:
            return

        if self.position == "Long":
            proceeds = price * self.quantity
            self.balance += proceeds
            pnl = (price - self.entry_price) * self.quantity
        else:  # Short
            cost = price * self.quantity
            self.balance -= cost
            pnl = (self.entry_price - price) * self.quantity

        self.trade_log.append({
            "time": time_stamp,
            "action": f"Close {self.position} ({reason})",
            "price": price,
            "quantity": self.quantity,
            "balance": self.balance,
            "pnl": pnl,
            "entry_price": self.entry_price,
            "stop_loss": self.stop_loss,
            "target_price": self.target_price
        })

        self.position = None
        self.entry_price = None
        self.quantity = 0
        self.stop_loss = None
        self.target_price = None
        self.balance_history.append(self.balance)

    def update_position(self, recommendation, price, time_stamp, stop_loss, target_price, risk_percent):
        """Update positions based on AI recommendation and price action."""
        # Check for stop loss/target hit
        if self.position == "Long":
            if price <= self.stop_loss:
                self.close_position(price, time_stamp, "Stop Loss")
            elif price >= self.target_price:
                self.close_position(price, time_stamp, "Target Reached")
        elif self.position == "Short":
            if price >= self.stop_loss:
                self.close_position(price, time_stamp, "Stop Loss")
            elif price <= self.target_price:
                self.close_position(price, time_stamp, "Target Reached")

        # Process new recommendation
        if recommendation == "Buy":
            if self.position != "Long":
                if self.position is not None:
                    self.close_position(price, time_stamp, "Position Change")
                self.open_position("Long", price, time_stamp, stop_loss, target_price, risk_percent)
        elif recommendation == "Sell":
            if self.position != "Short":
                if self.position is not None:
                    self.close_position(price, time_stamp, "Position Change")
                self.open_position("Short", price, time_stamp, stop_loss, target_price, risk_percent)
        elif recommendation == "Neutral":
            if self.position is not None:
                self.close_position(price, time_stamp, "Neutral Recommendation")

# --- Placeholder for StockAnalyzer and AIAnalyzer ---
class StockAnalyzer:
    def __init__(self, df):
        self.df = df

    def calculate_metrics(self):
        # Placeholder metrics calculation
        return {'rsi': 50, 'macd': 0.0, 'volume_change': 0.0}

    def analyze_trend(self):
        # Placeholder trend analysis
        return {'strength': 50}

class AIAnalyzer:
    def __init__(self):
        pass

    def generate_trading_recommendation(self, df, entry_price, stop_loss, target_price, metrics, trend, rr_buy, rr_sell):
        """
        Generates a trading recommendation based on analysis.
        This is a placeholder - replace with your actual AI logic.
        """
        if metrics['rsi'] < 30:
            return "Buy", "RSI Oversold", 2.5, 0.5
        elif metrics['rsi'] > 70:
            return "Sell", "RSI Overbought", 0.5, 2.5
        elif trend['strength'] > 60:
            return "Buy" if trend['strength'] > 0 else "Sell", "Trend Following", 1.5, 1.5
        else:
            return "Neutral", "No clear signal", 1.0, 1.0

# --- End Placeholder ---


def main():
    st.title("📈 Enhanced Trading Simulator with AI Analysis")

    # Initialize simulator
    if 'simulator' not in st.session_state:
        st.session_state.simulator = EnhancedSimulator()

    # Controls sidebar
    with st.sidebar:
        st.header("Simulation Controls")
        if st.button("🎲 Random Initial Balance (10k-100k)"):
            new_balance = np.random.randint(10000, 100000)
            st.session_state.simulator = EnhancedSimulator(new_balance)
            st.success(f"New balance: ${new_balance:,.2f}")

        risk_percent = st.slider("Risk Per Trade (%)", 0.1, 10.0, 2.0)
        symbol = st.selectbox("Select Asset", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"])
        st.write("## Trading Parameters")
        entry_price = st.number_input("Entry Price", value=100.0)
        stop_loss = st.number_input("Stop Loss", value=95.0)
        target_price = st.number_input("Target Price", value=110.0)

    # Main display
    chart_container = st.empty()
    metrics_container = st.expander("Live Metrics", expanded=True)
    simulation_container = st.expander("Simulation Details", expanded=True)

    # Initialize analyzers
    analyzer = StockAnalyzer(pd.DataFrame()) # Initialize with empty DataFrame initially
    ai_analyzer = AIAnalyzer()

    while True:
        try:
            df = get_live_data(symbol)
            if df.empty:
                time.sleep(5)
                continue

            # Update analyzer with new data
            analyzer.df = df

            # Update chart with trades
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']
            )])

            # Add trade markers
            simulator = st.session_state.simulator
            if simulator.trade_log:
                trades = pd.DataFrame(simulator.trade_log)
                for _, trade in trades.iterrows():
                    marker_color = 'green' if 'Long' in trade['action'] else 'red' if 'Short' in trade['action'] else 'blue'
                    fig.add_scatter(
                        x=[pd.to_datetime(trade['time'])],
                        y=[trade['price']],
                        mode='markers',
                        marker=dict(color=marker_color, size=12, symbol='diamond'),
                        name=trade['action']
                    )

            fig.update_layout(title=f"{symbol} Live Chart with Trades", height=600)
            chart_container.plotly_chart(fig, use_container_width=True, key="plot_chart") # Added key here

            # Generate trading signals
            metrics = analyzer.calculate_metrics()
            trend = analyzer.analyze_trend()
            current_price = df['Close'].iloc[-1]

            # Get AI recommendation
            recommendation, details, rr_buy, rr_sell = ai_analyzer.generate_trading_recommendation( # Call it from ai_analyzer instance
                df, entry_price, stop_loss, target_price, metrics, trend, 0, 0
            )

            # Update simulator
            sim_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.simulator.update_position(
                recommendation, current_price, sim_time,
                stop_loss, target_price, risk_percent
            )

            # Update metrics display
            with metrics_container:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Price", f"${current_price:.2f}")
                    st.metric("AI Recommendation", recommendation)
                with col2:
                    st.metric("RSI", f"{metrics['rsi']:.1f}")
                    st.metric("MACD", f"{metrics['macd']:.2f}")
                with col3:
                    st.metric("Volume Change", f"{metrics['volume_change']:.1f}%")
                    st.metric("Trend Strength", f"{trend['strength']:.1f}%")

            # Update simulation details
            with simulation_container:
                st.subheader("Account Overview")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Current Balance", f"${simulator.balance:,.2f}",
                             f"{((simulator.balance - simulator.initial_balance)/simulator.initial_balance*100):.1f}%")
                with col2:
                    if simulator.position:
                        pos_status = f"{simulator.position} {simulator.quantity} shares"
                        st.metric("Position", pos_status)
                        st.progress(abs(current_price - simulator.entry_price)/abs(simulator.target_price - simulator.entry_price))
                    else:
                        st.metric("Position", "Flat")

                # Performance metrics
                st.subheader("Performance Analysis")
                if simulator.trade_log:
                    trades_df = pd.DataFrame(simulator.trade_log)
                    wins = trades_df[trades_df['pnl'] > 0]

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total Trades", len(trades_df))
                    col2.metric("Win Rate", f"{len(wins)/len(trades_df)*100:.1f}%")
                    col3.metric("Avg Win", f"${wins['pnl'].mean():.1f}" if not wins.empty else "-")
                    col4.metric("Max Drawdown", f"{calculate_max_drawdown(simulator.balance_history):.1f}%")

                    # Balance curve
                    fig = go.Figure(go.Scatter(x=np.arange(len(simulator.balance_history)),
                                     y=simulator.balance_history, mode='lines'))
                    fig.update_layout(title="Account Balance History", height=300)
                    st.plotly_chart(fig, use_container_width=True, key="balance_chart") # Added key here

                # Trade log
                st.write("Recent Trades:")
                st.dataframe(trades_df.tail(5) if simulator.trade_log else pd.DataFrame())

            time.sleep(60)

        except Exception as e:
            st.error(f"Error: {str(e)}")
            time.sleep(10)

if __name__ == "__main__":
    main()