import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
# - MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://veninder47:3knoglq9RybLDj56@aiagentcluster.zdo9j.mongodb.net/')
DB_NAME = os.getenv('DB_NAME', 'stock_analysis')

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Application Settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')
