import random

from src.utils.helpers import get_spotify_link
from src.models import RecommendationModel
from src.constants import TRACK_NUM

def recommend_tracks(data: RecommendationModel):
    # Query Spotify API to search for the song and artist
    query = f"{data.input_values.prompt} {data.artist_name}"
    results = data.spotify_client.search(q=query, type='track', limit=1)

    # Proceed if the song is found
    if results['tracks']['items']:
        input_track = results['tracks']['items'][0]
        input_genre = data.input_values.trackId

        # Get audio analysis for the input track
        input_audio_analysis = data.spotify_client.audio_analysis(input_track['id'])
        
        # Modify tempo randomly within a range
        if data.input_values.tempo != 0:
            final_tempo = int(data.input_values.tempo)
        else:
            extracted_tempo = input_audio_analysis['track']['tempo'] + random.randint(-10,10)
            tempo_factor = random.randint(-10,10)
            input_tempo = extracted_tempo + tempo_factor
            final_tempo = (input_tempo + data.ordered_prompt["Tempo"])/2

        # Extract artist name and audio features
        input_audio_features = data.spotify_client.audio_features(input_track['id'])[0]

        # Modify energy randomly within a range but ensure it stays between 0 and 1
        if data.input_values.energy != 0:
            final_energy = float(data.input_values.energy)
        else:
            extracted_energy = input_audio_features['energy']
            energy_factor = random.uniform(-0.1, 0.1)
            input_energy = round(max(0, min(1, extracted_energy + energy_factor)), 3)
            final_energy = (input_energy + data.ordered_prompt["Energy"])/2

        # Similar modifications for valence, danceability, acousticness, and instrumentalness
        if data.input_values.mood_valence != 0:
            final_valence = float(data.input_values.mood_valence)
        else:
            extracted_valence = input_audio_features['valence']
            valence_factor = random.uniform(-0.1, 0.1)
            input_valence = round(max(0, min(1, extracted_valence + valence_factor)), 3)
            final_valence = (input_valence + data.ordered_prompt["Valence"])/2
        
        if data.input_values.danceability != 0:
            final_danceability = float(data.input_values.danceability)
        else:
            extracted_danceability = input_audio_features['danceability']
            danceability_factor = random.uniform(-0.1, 0.1)
            input_danceability = round(max(0, min(1, extracted_danceability + danceability_factor)), 3)
            final_danceability = (input_danceability + data.ordered_prompt["Danceability"])/2

        if data.input_values.acousticness != 0:
            final_acousticness = float(data.input_values.acousticness)
        else:
            extracted_acousticness = input_audio_features['acousticness']
            acousticness_factor = random.uniform(-0.1, 0.1)
            input_acousticness = round(max(0, min(1, extracted_acousticness + acousticness_factor)), 3)
            final_acousticness = (input_acousticness + data.ordered_prompt["Acousticness"])/2

        if data.input_values.instrumentalness != 0:
            final_instrumentalness = float(data.input_values.instrumentalness)
        else:
            extracted_instrumentalness = input_audio_features['instrumentalness']
            instrumentalness_factor = random.uniform(-0.1, 0.1)
            input_instrumentalness = round(max(0, min(1, extracted_instrumentalness + instrumentalness_factor)), 3)
            final_instrumentalness = (input_instrumentalness + data.ordered_prompt["Instrumentalness"])/2
        
        # Get recommendations based on the modified track features
        recommendations = data.spotify_client.recommendations(seed_genres=[data.ordered_prompt['Genre 1'].lower()], seed_artists=[input_genre], target_tempo=[final_tempo], target_energy=[final_energy], target_valence=[final_valence], target_danceability=[final_danceability], target_acousticness=[final_acousticness], target_instrumentalness=[final_instrumentalness], limit=TRACK_NUM)

        # Filter out the input track from the recommendations and truncate the list
        recommendations['tracks'] = [track for track in recommendations['tracks'] if track['id'] != input_track['id']]
        recommendations['tracks'] = recommendations['tracks'][:TRACK_NUM - 1]

        # Add Spotify URLs to the recommendations
        recommendations['spotify_url'] = [get_spotify_link(track['id'], data.spotify_client)['external_urls']['spotify'] for track in recommendations['tracks']]

        return recommendations
    
    else:
        print(f"No match found for the song '{data.input_values.prompt}'.")
        return None 