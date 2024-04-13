import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import random
from dotenv import load_dotenv
import os
import openai

from src.utils.recommend_tracks import recommend_tracks
from src.utils.order_prompt_input import order_prompt_input
from src.models import DataModel, RecommendationModel
from src.constants import SCOPE, TRACK_NUM

load_dotenv()

openai.api_key = os.getenv('OPENAI_KEY')
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
USERNAME = os.getenv('SPOTIFY_USERNAME')

# Initialize Spotify client with credentials
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

dictionary = {}

def generate(data: DataModel):
    
    # If user provides both prompt and trackId
    if data.prompt != "" and data.trackId != "":

        dictionary = order_prompt_input(data)

        # # Define scope for playlist modification and initialize SpotifyOAuth
        sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, username=USERNAME, redirect_uri='http://127.0.0.1:3000/')
        access_token = sp_oauth.get_access_token(as_dict=False)
        spotifyObject = spotipy.Spotify(auth=access_token)

        # Interactively create a playlist
        playlist_name = data.prompt
        playlist_description = "This is your playlist, created by Spotify Playlist Generator!"
        playlist = spotifyObject.user_playlist_create(user=USERNAME, name=playlist_name, public=True, description=playlist_description)
        playlist_id = playlist['id']

        # Prompt user for track and artist, then search and add the track to the playlist
        track = sp.track(data.trackId)        
        list_of_songs = []
        track_name = track['name']
        artist_name = track['artists'][0]['name']

        # Search for the track and add it to the playlist
        if artist_name:
            query = f"{track_name} {artist_name}"
        else:
            query = track_name
        result = spotifyObject.search(q=query)
        if len(result['tracks']['items']) > 0:
            list_of_songs.append(result['tracks']['items'][0]['uri'])
        else:
            print(f"No results found for '{track_name}' by '{artist_name}'")
        print(f"Added '{track_name}' by '{artist_name}' to the '{playlist_name}' playlist!")    
        
        # Generate and display recommendations based on the input track
        recommendation_data = RecommendationModel(
            input_values=data,
            song_name=track_name,
            artist_name=artist_name,
            spotify_client=sp,
            ordered_prompt=dictionary
        )
        recommendations = recommend_tracks(recommendation_data)

        if recommendations is not None:
            print(f"\nTop {TRACK_NUM} Recommendations:\n")
            for track in recommendations['tracks']:
                artists = ', '.join([artist['name'] for artist in track['artists']])
                list_of_songs.append(track['uri'])
                print(f"Added '{track['name']}' by '{artists}' to the '{playlist_name}' playlist!")

        # Add recommended tracks to the playlist
        spotifyObject.user_playlist_add_tracks(user=USERNAME, playlist_id=playlist_id, tracks=list_of_songs)
        
    elif data.prompt != "":  # This will only be checked if the first condition is False
        
        dictionary = order_prompt_input(data)

        list_of_songs = []

        # # Define scope for playlist modification and initialize SpotifyOAuth
        sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, username=USERNAME, redirect_uri='http://127.0.0.1:3000/')
        access_token = sp_oauth.get_access_token(as_dict=False)
        spotifyObject = spotipy.Spotify(auth=access_token)

        # Interactively create a playlist
        playlist_name = data.prompt
        playlist_description = "This is your playlist, created by Spotify Playlist Generator!"
        playlist = spotifyObject.user_playlist_create(user=USERNAME, name=playlist_name, public=True, description=playlist_description)
        playlist_id = playlist['id']

        # Modify tempo randomly within a range
        if data.tempo != 0:
            input_tempo = int(data.tempo)
        else:
            extracted_tempo = dictionary['Tempo']
            tempo_factor = random.randint(-10,10)
            input_tempo = extracted_tempo + tempo_factor

        # Modify energy randomly within a range but ensure it stays between 0 and 1
        if data.energy != 0:
            input_energy = float(data.energy)
        else:
            extracted_energy = dictionary['Energy']
            energy_factor = random.uniform(-0.1, 0.1)
            input_energy = round(max(0, min(1, extracted_energy + energy_factor)), 3)

        # Similar modifications for valence, danceability, acousticness, and instrumentalness
        if data.mood_valence != 0:
            input_valence = float(data.mood_valence)
        else:
            extracted_valence = dictionary['Valence']
            valence_factor = random.uniform(-0.1, 0.1)
            input_valence = round(max(0, min(1, extracted_valence + valence_factor)), 3)

        if data.danceability != 0:
            input_danceability = float(data.danceability)
        else:
            extracted_danceability = dictionary['Danceability']
            danceability_factor = random.uniform(-0.1, 0.1)
            input_danceability = round(max(0, min(1, extracted_danceability + danceability_factor)), 3)

        if data.acousticness != 0:
            input_acousticness = float(data.acousticness)
        else:
            extracted_acousticness = dictionary['Acousticness']
            acousticness_factor = random.uniform(-0.1, 0.1)
            input_acousticness = round(max(0, min(1, extracted_acousticness + acousticness_factor)), 3)

        if data.instrumentalness != 0:
            input_instrumentalness = float(data.instrumentalness)
        else:
            extracted_instrumentalness = dictionary['Instrumentalness']
            instrumentalness_factor = random.uniform(-0.1, 0.1)
            input_instrumentalness = round(max(0, min(1, extracted_instrumentalness + instrumentalness_factor)), 3)
            
        # Get recommendations based on the modified track features
        recommendations = sp.recommendations(seed_genres=[dictionary['Genre 1'].lower()], target_tempo=[input_tempo], target_energy=[input_energy], target_valence=[input_valence], target_danceability=[input_danceability], target_acousticness=[input_acousticness], target_instrumentalness=[input_instrumentalness], limit=TRACK_NUM)

        list_of_songs = [track['uri'] for track in recommendations['tracks']]

        spotifyObject.user_playlist_add_tracks(user=USERNAME, playlist_id=playlist_id, tracks=list_of_songs)

        print("Playlist Generated!")

    elif data.trackId != "":  # This will only be checked if the first and second conditions are False

        def get_spotify_link(track_id, sp):
            return sp.track(track_id)

        # Define a function to input track recommendations based on song name and artist name
        def input_track_recommendations(song_name, artist_name, sp):
            # Query Spotify API to search for the song and artist
            query = f"{song_name} {artist_name}"
            results = sp.search(q=query, type='track', limit=1)

            # Proceed if the song is found
            if results['tracks']['items']:
                input_track = results['tracks']['items'][0]
                input_genre = input_track['artists'][0]['id']

                audio_features = sp.audio_features(data.trackId)[0]
                print("\nTRACK INFO\n")
                print(audio_features)
                
                # Modify tempo randomly within a range
                if data.tempo is not None:
                    final_tempo = int(data.tempo)
                else:
                    extracted_tempo = audio_features['tempo'] + random.randint(-10,10)
                    tempo_factor = random.randint(-10,10)
                    input_tempo = extracted_tempo + tempo_factor
                    final_tempo = input_tempo

                # Modify energy randomly within a range but ensure it stays between 0 and 1
                if data.energy is not None:
                    final_energy = float(data.energy)
                else:
                    extracted_energy = audio_features['energy']
                    energy_factor = random.uniform(-0.1, 0.1)
                    input_energy = round(max(0, min(1, extracted_energy + energy_factor)), 3)
                    final_energy = input_energy

                # Similar modifications for valence, danceability, acousticness, and instrumentalness
                if data.mood_valence is not None:
                    final_valence = float(data.mood_valence)
                else:
                    extracted_valence = audio_features['valence']
                    valence_factor = random.uniform(-0.1, 0.1)
                    input_valence = round(max(0, min(1, extracted_valence + valence_factor)), 3)
                    final_valence = input_valence
                
                if data.danceability is not None:
                    final_danceability = float(data.danceability)
                else:
                    extracted_danceability = audio_features['danceability']
                    danceability_factor = random.uniform(-0.1, 0.1)
                    input_danceability = round(max(0, min(1, extracted_danceability + danceability_factor)), 3)
                    final_danceability = input_danceability

                if data.acousticness is not None:
                    final_acousticness = float(data.acousticness)
                else:
                    extracted_acousticness = audio_features['acousticness']
                    acousticness_factor = random.uniform(-0.1, 0.1)
                    input_acousticness = round(max(0, min(1, extracted_acousticness + acousticness_factor)), 3)
                    final_acousticness = input_acousticness

                if data.instrumentalness is not None:
                    final_instrumentalness = float(data.instrumentalness)
                else:
                    extracted_instrumentalness = audio_features['instrumentalness']
                    instrumentalness_factor = random.uniform(-0.1, 0.1)
                    input_instrumentalness = round(max(0, min(1, extracted_instrumentalness + instrumentalness_factor)), 3)
                    final_instrumentalness = input_instrumentalness
                
                # Get recommendations based on the modified track features
                recommendations = sp.recommendations(seed_artists=[input_genre], target_tempo=[final_tempo], target_energy=[final_energy], target_valence=[final_valence], target_danceability=[final_danceability], target_acousticness=[final_acousticness], target_instrumentalness=[final_instrumentalness], limit=track_num)

                # Filter out the input track from the recommendations and truncate the list
                recommendations['tracks'] = [track for track in recommendations['tracks'] if track['id'] != input_track['id']]
                recommendations['tracks'] = recommendations['tracks'][:track_num - 1]

                explicitActivate = True
                # While loop to filter out explicit tracks
                
                # Add Spotify URLs to the recommendations
                recommendations['spotify_url'] = [get_spotify_link(track['id'], sp)['external_urls']['spotify'] for track in recommendations['tracks']]

                return recommendations
            
            else:
                print(f"No match found for the song '{song_name}'.")
                return None  

        sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, username=USERNAME, redirect_uri='http://127.0.0.1:3000/')
        access_token = sp_oauth.get_access_token(as_dict=False)
        spotifyObject = spotipy.Spotify(auth=access_token)

        # Interactively create a playlist
        playlist_name = "Input-Only Playlist"
        playlist_description = "This is your playlist, created by Spotify Playlist Generator!"
        track_num = 50
        playlist = spotifyObject.user_playlist_create(user=USERNAME, name=playlist_name, public=True, description=playlist_description)
        playlist_id = playlist['id']

        # Prompt user for track and artist, then search and add the track to the playlist
        track = sp.track(data.trackId)        
        list_of_songs = []
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        # Search for the track and add it to the playlist
        if artist_name:
            query = f"{track_name} {artist_name}"
        else:
            query = track_name
        result = spotifyObject.search(q=query)
        if len(result['tracks']['items']) > 0:
            list_of_songs.append(result['tracks']['items'][0]['uri'])
        else:
            print(f"No results found for '{track_name}' by '{artist_name}'")
        print(f"Added '{track_name}' by '{artist_name}' to the '{playlist_name}' playlist!")           
        
        # Generate and display recommendations based on the input track
        recommendations = input_track_recommendations(track_name, artist_name, sp)

        if recommendations is not None:
            print(f"\nTop {track_num} Recommendations:\n")
            for track in recommendations['tracks']:
                artists = ', '.join([artist['name'] for artist in track['artists']])
                list_of_songs.append(track['uri'])
                print(f"Added '{track['name']}' by '{artists}' to the '{playlist_name}' playlist!")

        # Add recommended tracks to the playlist
        spotifyObject.user_playlist_add_tracks(user=USERNAME, playlist_id=playlist_id, tracks=list_of_songs)