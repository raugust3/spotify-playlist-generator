import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from .config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_USER_ID
)

# Function to initialize and return the Spotify client with client credentials
def init_spotipy_client():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to initialize and return the Spotify client with OAuth
def init_spotipy_oauth_client(scope=None):
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=scope
    )
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(f"Please navigate here in your browser: {auth_url}")
        response = input("Enter the URL you were redirected to: ")
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)

    return spotipy.Spotify(auth=token_info['access_token'])

# Define other Spotify-related functions here, such as creating a playlist,
# searching for tracks, adding tracks to a playlist, etc.

def create_playlist(name, description, public=True):
    sp = init_spotipy_oauth_client(scope='playlist-modify-public')
    user_id = SPOTIFY_USER_ID
    playlist = sp.user_playlist_create(user=user_id, name=name, public=public, description=description)
    return playlist

def search_tracks(query):
    sp = init_spotipy_client()
    return sp.search(q=query, type='track')

def add_tracks_to_playlist(playlist_id, track_uris):
    sp = init_spotipy_oauth_client(scope='playlist-modify-public')
    sp.playlist_add_items(playlist_id, track_uris)

def get_spotify_track_link(track_id):
    """Retrieve the Spotify track link."""
    sp = init_spotipy_client()
    try:
        track = sp.track(track_id)
        return track['external_urls']['spotify']
    except Exception as e:
        print(f"Error retrieving track link: {e}")
        return None

def get_track_recommendations(seed_artists=None, seed_genres=None, seed_tracks=None, **target_features):
    """Generate track recommendations based on seeds and target features."""
    sp = init_spotipy_client()
    try:
        recommendations = sp.recommendations(seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks, **target_features)
        return [track['uri'] for track in recommendations['tracks']]
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return []
