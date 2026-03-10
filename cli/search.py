import json
from pathlib import Path
import string

def remove_punctuations_translate(input_string):
    # Create a translation table that maps every punctuation character to None
    translator = str.maketrans('', '', string.punctuation)
    # Use the translate method to remove all characters in the translation table
    clean_string = input_string.translate(translator)
    return clean_string


def search(query, max_result):
    data_path = Path(__file__).resolve().parent.parent / "data" / "movies.json"
    with open(data_path, "r") as file:
        movie_data = json.load(file)
    results = []
    for movie in movie_data.get("movies", []):
        title = movie.get("title", "")
        if remove_punctuations_translate(query).lower() in remove_punctuations_translate(title).lower():
            results.append(movie)
            if len(results) >= max_result:
                break

    return results




 