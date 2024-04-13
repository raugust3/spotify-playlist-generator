from pydantic import BaseModel
from spotipy import Spotify

class DataModel(BaseModel):
    acousticness: str
    danceability: str
    energy: str
    instrumentalness: str
    mood_valence: str
    tempo: str
    prompt: str
    trackId: str

class GenerateModel(BaseModel):
    input_values: DataModel
    spotify_client: Spotify
    spotify_username: str
    spotify_id: str
    spotify_secret: str

    class Config:
        arbitrary_types_allowed = True

class RecommendationModel(BaseModel):
    input_values: DataModel
    song_name: str
    artist_name: str
    spotify_client: Spotify
    ordered_prompt: dict

    class Config:
        arbitrary_types_allowed = True