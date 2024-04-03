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
        # Remove punctuation from the prompt
        final_prompt = prompt.translate(translator)
        
        genre_prompt = (f"You are a playlist curator for Spotify. You are given this prompt: '{final_prompt}'. "
                        "As a curator, pick the most relevant genre to this prompt ONLY FROM THIS LIST. "
                        "If the genre that you pick is not in the list, choose the most similar one from the list: \n\n"
                        + "\n".join(genres_list))

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=genre_prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7
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
