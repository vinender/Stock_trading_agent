# AI-Powered Stock Market Analysis

An advanced AI-powered stock analysis platform for Indian markets, leveraging machine learning and real-time data processing to provide comprehensive financial insights.

## Features
- Real-time stock data analysis
- Technical indicators calculation
- AI-powered market insights
- Pattern recognition
- Interactive visualizations

## Prerequisites
- Python 3.11 or higher
- MongoDB (local installation or MongoDB Atlas account)
- OpenAI API key

## Local Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd stock-analysis
```

2. Install required packages:
```bash
pip install streamlit pandas yfinance plotly langchain langchain-community openai ta pymongo python-dotenv
```

3. Set up MongoDB:
- Install MongoDB locally or create a MongoDB Atlas account
- Create a new database named 'stock_analysis'

4. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the values in `.env` with your configurations:
  - Set your MongoDB connection URI
  - Add your OpenAI API key
  - Adjust other settings as needed

5. Run the application:
```bash
streamlit run main.py
```

The application will be available at `http://localhost:5000`

## Project Structure
- `main.py`: Main Streamlit application
- `stock_analyzer.py`: Stock analysis logic
- `ai_analyzer.py`: AI-powered analysis using LangChain
- `patterns.py`: Technical pattern recognition
- `utils.py`: Utility functions
- `database.py`: MongoDB connection and operations
- `config.py`: Configuration management

## Development Guidelines
- Use Python type hints for better code readability
- Follow PEP 8 style guidelines
- Add appropriate error handling
- Keep functions focused and modular
- Add logging for debugging

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
