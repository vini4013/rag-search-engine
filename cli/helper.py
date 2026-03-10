import json


def load_json(path):
	with open(path, "r") as file:
		return json.load(file)


def load_stop_words(path):
	with open(path, "r") as file:
		return file.read().splitlines()
