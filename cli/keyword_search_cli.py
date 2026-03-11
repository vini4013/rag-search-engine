#!/usr/bin/env python3

import argparse
import sys
from search import search
from inverted_index import InvertedIndex
from helper import load_json
from constants import DATA_PATH


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")
    subparsers.add_parser("build", help="Build and save inverted index")
    tf_parser = subparsers.add_parser("tf", help="Get term frequency for a document")
    tf_parser.add_argument("doc_id", type=int, help="Document ID")
    tf_parser.add_argument("term", type=str, help="Term to check")
    idf_parser = subparsers.add_parser("idf", help="Get inverse document frequency for a term")
    idf_parser.add_argument("term", type=str, help="Term to check")
    tfidf_parser = subparsers.add_parser("tfidf", help="Get TF-IDF for a term in a document")
    tfidf_parser.add_argument("doc_id", type=int, help="Document ID")
    tfidf_parser.add_argument("term", type=str, help="Term to check")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            results = search(args.query, max_result=5)
            for index, movie in enumerate(results, start=1):
                print(f"{index}. {movie.get('title', '')} ({movie.get('id', '')})")
        case "build":
            movie_data = load_json(DATA_PATH)
            movies = movie_data.get("movies", [])
            inverted_index = InvertedIndex()
            inverted_index.build(movies)
            inverted_index.save()
            print("Inverted index built and saved successfully.")
        case "tf":
            inverted_index = InvertedIndex()
            inverted_index.load()
            print(inverted_index.get_tf(args.doc_id, args.term))
        case "idf":
            inverted_index = InvertedIndex()
            inverted_index.load()
            idf = inverted_index.get_idf(args.term)
            print(f"Inverse document frequency of '{args.term}': {idf:.2f}")
        case "tfidf":
            inverted_index = InvertedIndex()
            inverted_index.load()
            tfidf = inverted_index.get_tfidf(args.doc_id, args.term)
            print(f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tfidf:.2f}")       
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()

   