from pymongo import MongoClient
from config import MONGODB_URI, DB_NAME
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(MONGODB_URI)
            self.db = self.client[DB_NAME]
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {str(e)}")
            raise

    def save_stock_analysis(self, stock_symbol, analysis_data):
        """Save stock analysis results to MongoDB"""
        try:
            collection = self.db.stock_analyses
            analysis_data['stock_symbol'] = stock_symbol
            analysis_data['timestamp'] = datetime.now()
            result = collection.insert_one(analysis_data)
            logger.info(f"Analysis saved for {stock_symbol}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error saving analysis: {str(e)}")
            raise

    def get_stock_analysis(self, stock_symbol):
        """Retrieve latest stock analysis from MongoDB"""
        try:
            collection = self.db.stock_analyses
            return collection.find_one(
                {'stock_symbol': stock_symbol},
                sort=[('timestamp', -1)]
            )
        except Exception as e:
            logger.error(f"Error retrieving analysis: {str(e)}")
            raise

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
