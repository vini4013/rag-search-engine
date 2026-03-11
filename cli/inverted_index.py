import pickle
from pathlib import Path
from collections import Counter
from helper import preprocess_into_tokens
import math
from constants import TOTAL_DOC_COUNT


class InvertedIndex:
    index: dict[str, set[int]]
    docmap: dict[int, dict]
    term_frequencies: dict[int, Counter]

    def __init__(self):
        self.index = {}
        self.docmap = {}
        self.term_frequencies = {}

    def __add_document(self, doc_id, text):
        tokens = preprocess_into_tokens(text)
        if doc_id not in self.term_frequencies:
            self.term_frequencies[doc_id] = Counter()

        for token in tokens:
            self.term_frequencies[doc_id][token] += 1
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def build(self, movies):
        self.index = {}
        self.docmap = {}
        self.term_frequencies = {}

        for m in movies:
            doc_id = m["id"]
            doc_description = f"{m['title']} {m['description']}"
            self.docmap[doc_id] = m
            self.__add_document(doc_id, doc_description)

    def get_documents(self, term):
        normalized_term = term.lower()
        documents = self.index.get(normalized_term, set())
        return sorted(documents)

    def get_tf(self, doc_id, term):
        tokens = preprocess_into_tokens(term)
        if len(tokens) != 1:
            raise ValueError("Term must preprocess into exactly one token")

        token = tokens[0]
        if doc_id not in self.term_frequencies:
            return 0

        return self.term_frequencies[doc_id].get(token, 0)
    
    def get_idf(self, term):
        tokens = preprocess_into_tokens(term)
        if len(tokens) != 1:
            raise ValueError("Term must preprocess into exactly one token")
        
        token = tokens[0]
        doc_freq = len(self.index.get(token, set()))
        return math.log((TOTAL_DOC_COUNT + 1) / (doc_freq + 1))

    def save(self):
        cache_dir = Path("cache")
        cache_dir.mkdir(parents=True, exist_ok=True)

        index_path = cache_dir / "index.pkl"
        docmap_path = cache_dir / "docmap.pkl"
        term_frequencies_path = cache_dir / "term_frequencies.pkl"

        with open(index_path, "wb") as file:
            pickle.dump(self.index, file)

        with open(docmap_path, "wb") as file:
            pickle.dump(self.docmap, file)

        with open(term_frequencies_path, "wb") as file:
            pickle.dump(self.term_frequencies, file)

    def load(self):
        index_path = Path("cache") / "index.pkl"
        docmap_path = Path("cache") / "docmap.pkl"
        term_frequencies_path = Path("cache") / "term_frequencies.pkl"

        if not index_path.exists():
            raise FileNotFoundError(f"Missing index cache file: {index_path}")
        if not docmap_path.exists():
            raise FileNotFoundError(f"Missing docmap cache file: {docmap_path}")
        if not term_frequencies_path.exists():
            raise FileNotFoundError(f"Missing term frequencies cache file: {term_frequencies_path}")

        with open(index_path, "rb") as file:
            self.index = pickle.load(file)

        with open(docmap_path, "rb") as file:
            self.docmap = pickle.load(file)

        with open(term_frequencies_path, "rb") as file:
            self.term_frequencies = pickle.load(file)