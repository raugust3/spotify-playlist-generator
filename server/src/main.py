from fastapi import FastAPI, HTTPException
from .config import APP_DESCRIPTION, APP_VERSION, CORS_ORIGINS
from .models import DataModel  # Assuming you have a separate file for Pydantic models called models.py
from .playlist_generator import generate_playlist
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Spotify Playlist Generator API", description=APP_DESCRIPTION, version=APP_VERSION)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return {"message": "Welcome to the Spotify Playlist Generator API!"}

@app.post("/generate_playlist", response_model=DataModel)
async def create_playlist_endpoint(data: DataModel):
    try:
        # Generate the playlist with the provided details.
        # This assumes that your DataModel includes a field for `prompt` and any other necessary data.
        playlist_id = generate_playlist(data.user_id, data.prompt, data.genres_list, data.track_num)

        return {
            "status": "success",
            "playlist_id": playlist_id
        }

    except ValueError as e:
        # Handle specific exceptions raised from within generate_playlist
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Catch all other exceptions and return a generic error message.
        # You might want to log this exception.
        raise HTTPException(status_code=500, detail="An error occurred while generating the playlist.")

# Add other endpoints as necessary

