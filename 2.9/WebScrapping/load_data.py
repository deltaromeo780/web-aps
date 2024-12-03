from mongoengine import connect
import json
import os
from models import Author, Quote
from dotenv import load_dotenv

# Wczytaj zmienne środowiskowe z pliku .env
load_dotenv()


def load_data_to_db():
    # Połącz z bazą danych MongoDB Atlas

    MONGODB_URI = os.getenv("MONGODB_URI")
    DB_NAME = os.getenv("DB_NAME")

    connect(host=MONGODB_URI, db=DB_NAME, ssl=True)

    # Wczytaj dane z plików JSON
    with open('authors.json', 'r') as file:
        authors_data = json.load(file)

    with open('quotes.json', 'r') as file:
        quotes_data = json.load(file)

    # Zapisz dane do bazy danych
    for author_data in authors_data:
        author = Author.objects(fullname=author_data['fullname']).first()
        if not author:
            author = Author(**author_data)
            author.save()

    for quote_data in quotes_data:
        author = Author.objects(fullname=quote_data['author']).first()
        if author:
            quote = Quote(**quote_data)
            quote.author = author
            quote.save()


if __name__ == "__main__":
    load_data_to_db()


# from mongoengine import connect
# import json
# from models import Author, Quote
#
#
# def load_data_to_db():
#     # Połącz z bazą danych MongoDB Atlas
#     connect(host="mongodb+srv://paull:ania_783006@cluster00.25gaxen.mongodb.net/", db="homework_nine", ssl=True)
#
#     # Wczytaj dane z plików JSON
#     with open('authors.json', 'r') as file:
#         authors_data = json.load(file)
#
#     with open('quotes.json', 'r') as file:
#         quotes_data = json.load(file)
#
#     # Zapisz dane do bazy danych
#     for author_data in authors_data:
#         author = Author(**author_data)
#         author.save()
#
#     for quote_data in quotes_data:
#         quote = Quote(**quote_data)
#         quote.author = Author.objects(author=quote_data['author']).first()
#         quote.save()
#
#
# if __name__ == "__main__":
#     load_data_to_db()
