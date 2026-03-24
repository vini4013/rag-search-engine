#!/usr/bin/env python3

import argparse
import sys
from search import search
from inverted_index import InvertedIndex
from helper import load_json
from constants import BM25_K1, DATA_PATH


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
    bm25_idf_parser = subparsers.add_parser("bm25idf", help="Get BM25 IDF score for a given term")
    bm25_idf_parser.add_argument("term", type=str, help="Term to get BM25 IDF score for")
    bm25_tf_parser = subparsers.add_parser("bm25tf", help="Get BM25 TF score for a given document ID and term")
    bm25_tf_parser.add_argument("doc_id", type=int, help="Document ID")
    bm25_tf_parser.add_argument("term", type=str, help="Term to get BM25 TF score for")
    bm25_tf_parser.add_argument("k1", type=float, nargs='?', default=BM25_K1, help="Tunable BM25 K1 parameter")
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
        case "bm25idf":
            inverted_index = InvertedIndex()
            inverted_index.load()
            bm25_idf = inverted_index.get_bm25_idf(args.term)
            print(f"BM25 IDF score of '{args.term}': {bm25_idf:.2f}")  
        case "bm25tf":    
            inverted_index = InvertedIndex()
            inverted_index.load()
            bm25_tf = inverted_index.get_bm25_tf(args.doc_id, args.term, args.k1)
            print(f"BM25 TF score of '{args.term}' in document '{args.doc_id}': {bm25_tf:.2f}")
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()

   