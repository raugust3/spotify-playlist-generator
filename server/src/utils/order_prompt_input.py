import string
import openai

from src.utils.helpers import create_prompt
from src.constants import GENRE_LIST
from src.models import DataModel

def order_prompt_input(data: DataModel):
    # Create a translation table to replace punctuation with None
    translator = str.maketrans('', '', string.punctuation)
    # Remove punctuation from the string
    final_prompt = data.prompt.translate(translator)
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=create_prompt(final_prompt, GENRE_LIST)
    )

    response_content = str(response.choices[0].message)

    # Extracting the content from the response string
    start = response_content.find("content='") + 9
    end = response_content.find("', role='")
    actual_content = response_content[start:end]

    # Splitting the actual content by newline to get each attribute line
    attribute_lines = actual_content.split("\\n")

    # Parsing each line and filling the dictionary
    dictionary = {}
    for line in attribute_lines:
        # Splitting each line into key and value
        key_value = line.split(": ")
        if len(key_value) == 2:
            # Assigning to dictionary, converting numeric values when necessary
            key, value = key_value
            if key in ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Tempo', 'Valence']:
                try:
                    dictionary[key] = float(value) if '.' in value else int(value)
                except ValueError:
                    dictionary[key] = value  # In case of conversion error, keep original string
            else:
                dictionary[key] = value

    dictionary["Genre 1"] = dictionary["Genre 1"].strip()

    print(dictionary)

    if dictionary["Genre 1"] not in GENRE_LIST:
        dictionary["Genre 1"] = "Pop"
    
    return dictionary