from pydantic import BaseModel

class DataModel(BaseModel):
    acousticness: str
    danceability: str
    energy: str
    instrumentalness: str
    mood_valence: str
    tempo: str
    prompt: str
    trackId: str