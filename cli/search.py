import sys
from nltk.stem import PorterStemmer
from helper import preprocess_into_tokens
from inverted_index import InvertedIndex


def search(query, max_result):
    inverted_index = InvertedIndex()
    try:
        inverted_index.load()
    except FileNotFoundError as error:
        print(f"Error: {error}")
        sys.exit(1)

    query_tokens = preprocess_into_tokens(query)
    result_ids = []
    seen_ids = set()

    for token in query_tokens:
        matching_documents = inverted_index.get_documents(token)
        for doc_id in matching_documents:
            if doc_id in seen_ids:
                continue

            seen_ids.add(doc_id)
            result_ids.append(doc_id)

            if len(result_ids) >= max_result:
                break


    return [inverted_index.docmap[doc_id] for doc_id in result_ids if doc_id in inverted_index.docmap]




 