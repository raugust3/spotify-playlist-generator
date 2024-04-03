import os
from dotenv import load_dotenv

# Load environment variables from .env file at the project root
load_dotenv()

# Spotify API Credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')  
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')  

# OpenAI API Key
OPENAI_API_KEY = os.getenv('openai.api_key') 

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
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:3001/callback')  # Change to your application's redirect URI

# Spotify User
SPOTIFY_USER_ID = '31vxd2rpgrlanjxy6mu5fvcexoaq'  # Your Spotify user ID

# Application Settings
APP_DESCRIPTION = "Spotify Playlist Generator API"
APP_VERSION = "1.0.0"

# Add other configurations as necessary
