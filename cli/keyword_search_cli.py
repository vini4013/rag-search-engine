#!/usr/bin/env python3

import argparse
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

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            results = search(args.query, max_result=5)
            for index, movie in enumerate(results, start=1):
                print(f"{index}. {movie.get('title', '')}")
        case "build":
            movie_data = load_json(DATA_PATH)
            movies = movie_data.get("movies", [])

            inverted_index = InvertedIndex()
            inverted_index.build(movies)
            inverted_index.save()

            merida_documents = inverted_index.get_documents("merida")
            first_document_id = merida_documents[0] if merida_documents else None
            print(f"First document for token 'merida' = {first_document_id}")
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()

   