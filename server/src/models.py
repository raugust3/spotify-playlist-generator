from pydantic import BaseModel, Field
from typing import List, Optional

class DataModel(BaseModel):
    prompt: str
    genres_list: List[str]
    user_id: str
    track_num: Optional[int] = 50  # Default to 50 if not provided

    class Config:
        schema_extra = {
            "example": {
                "prompt": "Chill vibes for coding",
                "genres_list": ["chill", "lofi", "ambient"],
                "user_id": "your_spotify_user_id",
                "track_num": 20
            }
        }
