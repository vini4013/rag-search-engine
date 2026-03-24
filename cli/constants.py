from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "movies.json"
STOPWORDS_PATH = ROOT_DIR / "data" / "stopwords.txt"
BM25_K1 = 1.5
