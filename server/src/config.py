import os
from dotenv import load_dotenv

# Load environment variables from .env file at the project root
load_dotenv()

# Spotify API Credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')  # Replace 'your-default-client-id' with a default or raise an exception if this should not have a default
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')  # Same as above

# OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-default-openai-key')  # Same as above

# CORS configuration
CORS_ORIGINS = [
    "http://localhost:3001",  # Local development frontend
]

# Security configurations
# It's better to set these to False if not in a development environment
DEBUG = os.getenv('DEBUG', 'False') == 'True'  # Example: Convert the string 'True' from .env to a boolean True
ALLOW_ALL_ORIGINS = os.getenv('ALLOW_ALL_ORIGINS', 'False') == 'True'

# Playlist Generator Configurations
DEFAULT_GENRE = "pop"
TRACK_NUM = 50  # Number of tracks in the playlist

# Spotify Redirect URI
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:3000/callback')  # Change to your application's redirect URI

# Spotify User
SPOTIFY_USER_ID = os.getenv('SPOTIFY_USER_ID')  # Your Spotify user ID

# Application Settings
APP_DESCRIPTION = "Spotify Playlist Generator API"
APP_VERSION = "1.0.0"

# Add other configurations as necessary
