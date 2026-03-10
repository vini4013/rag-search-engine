import string
from nltk.stem import PorterStemmer
from helper import load_json, load_stop_words

from constants import DATA_PATH, STOPWORDS_PATH

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

def stem_tokens(tokens):
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]

def preprocess_tokens(input_string, stop_words):
    normalized_input = remove_punctuations_translate(input_string).lower()
    tokens = split_into_tokens(normalized_input)
    filtered_tokens = remove_stopwords(tokens, stop_words)
    return stem_tokens(filtered_tokens)

def search(query, max_result):
    movie_data = load_json(DATA_PATH)
    stop_words = load_stop_words(STOPWORDS_PATH)
    stop_words_set = set(stop_words)
    query_tokens = preprocess_tokens(query, stop_words_set)

    results = []
    for movie in movie_data.get("movies", []):
        title = movie.get("title", "")
        title_tokens = preprocess_tokens(title, stop_words_set)

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




 