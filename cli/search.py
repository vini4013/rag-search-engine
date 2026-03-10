import json
from pathlib import Path
import string

def remove_punctuations_translate(input_string):
    # Create a translation table that maps every punctuation character to None
    translator = str.maketrans('', '', string.punctuation)
    # Use the translate method to remove all characters in the translation table
    clean_string = input_string.translate(translator)
    return clean_string

def split_into_tokens(input_string):
    return [x for x in input_string.split(' ') if x]

def remove_stopwords(tokens, stop_words):
    return [token for token in tokens if token not in stop_words]

def search(query, max_result):
    data_path = Path(__file__).resolve().parent.parent / "data" / "movies.json"
    stopwords_path = Path(__file__).resolve().parent.parent / "data" / "stopwords.txt"

    with open(data_path, "r") as file:
        movie_data = json.load(file)
    with open(stopwords_path, "r") as file:
        stop_words = file.read().splitlines()

    stop_words_set = set(stop_words)

    normalized_query = remove_punctuations_translate(query).lower()
    query_tokens = remove_stopwords(split_into_tokens(normalized_query), stop_words_set)

    results = []
    for movie in movie_data.get("movies", []):
        title = movie.get("title", "")
        normalized_title = remove_punctuations_translate(title).lower()
        title_tokens = remove_stopwords(split_into_tokens(normalized_title), stop_words_set)

        has_token_match = any(
            query_token in title_token
            for query_token in query_tokens
            for title_token in title_tokens
        )

        if has_token_match:
            results.append(movie)
            if len(results) >= max_result:
                break

    return results




 