import pickle
from pathlib import Path


class InvertedIndex:
    index: dict[str, set[int]]
    docmap: dict[int, dict]

    def __init__(self):
        self.index = {}
        self.docmap = {}

    def __add_document(self, doc_id, text):
        for word in text.split():
            normalized_word = word.lower()
            if normalized_word not in self.index:
                self.index[normalized_word] = set()
            self.index[normalized_word].add(doc_id)

    def build(self, movies):
        self.index = {}
        self.docmap = {}

        for movie in movies:
            doc_id = movie["id"]
            self.docmap[doc_id] = movie
            self.__add_document(doc_id, f"{movie['title']} {movie['description']}")

    def get_documents(self, term):
        normalized_term = term.lower()
        documents = self.index.get(normalized_term, set())
        return sorted(documents)

    def save(self):
        cache_dir = Path("cache")
        cache_dir.mkdir(parents=True, exist_ok=True)

        index_path = cache_dir / "index.pkl"
        docmap_path = cache_dir / "docmap.pkl"

        with open(index_path, "wb") as file:
            pickle.dump(self.index, file)

        with open(docmap_path, "wb") as file:
            pickle.dump(self.docmap, file)

    def load(self):
        index_path = Path("cache") / "index.pkl"
        docmap_path = Path("cache") / "docmap.pkl"

        if not index_path.exists():
            raise FileNotFoundError(f"Missing index cache file: {index_path}")
        if not docmap_path.exists():
            raise FileNotFoundError(f"Missing docmap cache file: {docmap_path}")

        with open(index_path, "rb") as file:
            self.index = pickle.load(file)

        with open(docmap_path, "rb") as file:
            self.docmap = pickle.load(file)