from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "movies.json"
STOPWORDS_PATH = ROOT_DIR / "data" / "stopwords.txt"
TOTAL_DOC_COUNT = 5000
