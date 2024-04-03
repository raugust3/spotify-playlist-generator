from pydantic import BaseModel, Field
from typing import List, Optional

class DataModel(BaseModel):
    acousticness: str
    danceability: str
    energy: str
    instrumentalness: str
    mood_valence: str
    tempo: str
    prompt: str
    trackId: str

    class Config:
        schema_extra = {
            "example": {
                "prompt": "Chill vibes for coding",
                "genres_list": ["chill", "lofi", "ambient"],
                "user_id": '31vxd2rpgrlanjxy6mu5fvcexoaq',
                "track_num": 20
            }
        }
