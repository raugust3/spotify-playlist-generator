import openai
from .config import OPENAI_API_KEY
import string

# Ensure the OpenAI API key is set
openai.api_key = OPENAI_API_KEY

def generate_playlist_details_from_prompt(prompt, genres_list):
    """
    Uses OpenAI to generate playlist attributes based on a given prompt.
    
    Args:
        prompt (str): The prompt describing the type of playlist desired.
        genres_list (list): The list of genres available for playlist creation.
        
    Returns:
        dict: A dictionary with playlist attributes including genre, acousticness,
              danceability, energy, instrumentalness, tempo, and valence.
    """
    try:
        # Create a translation table to replace punctuation with None
        translator = str.maketrans('', '', string.punctuation)
        # Remove punctuation from the string
        final_prompt = prompt.translate(translator)

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (f"You are a playlist curator for Spotify. You are given this prompt: '{final_prompt}'. As a curator, pick the most relevant genre to this prompt ONLY FROM THIS LIST. If the genre that you pick is not in the list, choose the most similar one from the list: \n" + genres_list +
                                "\nAlso, assign values to the following track attributes: \n\n"
                                "Acousticness: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic. Range: 0 - 1. \n\n"
                                "Danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. \n\n"
                                "Energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. \n\n"
                                "Instrumentalness: Predicts whether a track contains no vocals. \"Ooh\" and \"aah\" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly \"vocal\". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0. \n\n"
                                "Tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. Range: 60 - 180. \n\n"
                                "Valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). Range: 0 - 1. \n\n"
                                "Give me your response in the following format, and do not deviate from it: \n"                      
                                "Acousticness: <Acousticness Value> \n"
                                "Danceability: <Danceability Value> \n"
                                "Energy: <Energy Value> \n"
                                "Instrumentalness: <Instrumentalness Value> \n"
                                "Tempo: <Tempo Value> \n"
                                "Valence: <Valence Value>\n"
                                "Genre 1: <Genre #1> \n")
                },
            ]
        )
        response_text = response.choices[0].text.strip()

        # Assuming the response_text is properly formatted to parse into a dictionary
        attributes = parse_openai_response_to_dict(response_text)

        return attributes

    except Exception as e:
        print(f"Error generating playlist details from prompt: {e}")
        return {}

def parse_openai_response_to_dict(response_text):
    """
    Parses the response text from OpenAI into a dictionary of attributes.
    
    Args:
        response_text (str): The raw string response from OpenAI.
        
    Returns:
        dict: A dictionary containing the parsed attributes.
    """
    # Here, parse the response text into a dictionary
    # This will depend on the expected format of your response
    # For example, if your response is in the form of "Attribute: Value", you can do:
    attributes = {}
    for line in response_text.split('\n'):
        key, value = line.split(': ')
        attributes[key.strip().lower().replace(' ', '_')] = value.strip()
    
    return attributes
