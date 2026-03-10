import json
import string
from nltk.stem import PorterStemmer
from constants import STOPWORDS_PATH


def load_json(path):
	with open(path, "r") as file:
		return json.load(file)


def load_stop_words(path):
	with open(path, "r") as file:
		return file.read().splitlines()
	
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

def preprocess_into_tokens(input_string):
    stop_words = load_stop_words(STOPWORDS_PATH)
    stop_words_set = set(stop_words)
    normalized_input = remove_punctuations_translate(input_string).lower()
    tokens = split_into_tokens(normalized_input)
    filtered_tokens = remove_stopwords(tokens, stop_words_set)
    return stem_tokens(filtered_tokens)
