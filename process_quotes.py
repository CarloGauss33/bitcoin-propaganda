import json
import random

class Quote:
    def __init__(self, text, medium, date) -> None:
        self.text = text
        self.medium = medium
        self.date = date

    def __str__(self) -> str:
        return f'"{self.text}"\nSatoshi Nakamoto. ({self.date}). {self.medium}'

    @classmethod
    def from_dict(cls, dictionary):
        return Quote(dictionary['text'], dictionary['medium'], dictionary['date'])

class QuoteManager:
    def __init__(self, quotes_path) -> None:
        with open(quotes_path) as file:
            raw_quotes = json.load(file)
        self.quotes = [Quote.from_dict(dict_quote) for dict_quote in raw_quotes]

    def get_random_quote(self) -> Quote:
        return random.choice(self.quotes)
