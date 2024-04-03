from .spotify_api import create_playlist, search_tracks, add_tracks_to_playlist
from .openai_api import generate_playlist_details_from_prompt

def generate_playlist(user_id, prompt, genres_list, track_num=50):
    """
    Generates a playlist based on a prompt using the OpenAI API and Spotify API.

    Args:
        user_id (str): The Spotify user ID for whom the playlist is created.
        prompt (str): The prompt describing the desired mood/attributes of the playlist.
        genres_list (list): A list of genres to select from for playlist creation.
        track_num (int): The number of tracks to include in the playlist.

    Returns:
        str: The Spotify URI of the created playlist.
    """
    # Generate the playlist details from the prompt using OpenAI
    playlist_details = generate_playlist_details_from_prompt(prompt, genres_list)

    if not playlist_details:
        raise ValueError("Failed to generate playlist details from the prompt.")

    # Use the details from OpenAI to create a playlist and get tracks
    playlist = create_playlist(user_id, f"Playlist: {prompt}", "Generated by Spotify Playlist Generator")

    if not playlist:
        raise ValueError("Failed to create a playlist on Spotify.")

    playlist_id = playlist['id']

    # Based on the details, search for tracks
    genre = playlist_details.get('genre', None)
    tracks = search_tracks(genre) if genre else []

    if not tracks:
        raise ValueError(f"No tracks found for the genre: {genre}")

    # Assuming tracks is a list of track URIs
    track_uris = [track['uri'] for track in tracks['items'][:track_num]]

    # Add the tracks to the playlist
    add_tracks_to_playlist(playlist_id, track_uris)

    return playlist_id