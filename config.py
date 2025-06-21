import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for SmartLearn application"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///smartlearn.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Services Configuration
    ENABLE_AI_CLASSIFICATION = os.getenv("ENABLE_AI_CLASSIFICATION", "true").lower() == "true"
    ENABLE_OLLAMA = os.getenv("ENABLE_OLLAMA", "true").lower() == "true"
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    
    # External APIs
    GOOGLE_BOOKS_API_ENABLED = os.getenv("GOOGLE_BOOKS_API_ENABLED", "true").lower() == "true"
    YOUTUBE_API_ENABLED = os.getenv("YOUTUBE_API_ENABLED", "true").lower() == "true"
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Feature Flags
    ENABLE_COMMUNITY_FEATURES = os.getenv("ENABLE_COMMUNITY_FEATURES", "true").lower() == "true"
    ENABLE_AI_VIDEO_SEARCH = os.getenv("ENABLE_AI_VIDEO_SEARCH", "true").lower() == "true" 