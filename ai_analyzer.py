from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os

class AIAnalyzer:
    def __init__(self):
        self.prompt_template = PromptTemplate(
            input_variables=["stock_data"],
            template="""
            Analyze the following Indian stock market data and provide insights:
            {stock_data}

            Please provide:
            1. Overall market sentiment (bullish/bearish)
            2. Key candlestick patterns identified
            3. Potential support and resistance levels
            4. Short-term trading recommendation with rationale
            5. Based on the data, what is the likely price movement in the next 5 trading days?
            6. Important technical indicators (RSI, MACD)
            """
        )

        self.llm = OpenAI(temperature=0.7)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def analyze_stock(self, df):
        """Analyze stock data using LangChain"""
        # Prepare data for analysis
        last_week = df.tail(5).to_string()
        latest_close = df['Close'].iloc[-1]
        latest_volume = df['Volume'].iloc[-1]

        # Prepare analysis context
        analysis_data = f"""
        Last 5 days trading data:
        {last_week}

        Latest Close Price: {latest_close:.2f}
        Latest Trading Volume: {latest_volume:,}
        """

        # Get AI analysis
        analysis = self.chain.run(stock_data=analysis_data)
        return analysis

    def get_pattern_prediction(self, pattern):
        """Get specific prediction based on identified pattern"""
        prompt = f"""Given the {pattern} pattern observed in Indian stock market context:
        1. What is the typical success rate of this pattern?
        2. What are the key price levels to watch?
        3. What is the recommended trading strategy?
        4. 
        """
        return self.llm.predict(prompt)