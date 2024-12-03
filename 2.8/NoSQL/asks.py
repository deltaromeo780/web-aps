from models import Quote, Author
from mongoengine import connect

connect(host="mongodb+srv://paull:ania_783006@cluster00.25gaxen.mongodb.net/", db="homework", ssl=True)


def search_quotes(query):
    if query.startswith('name:'):
        author_name = query.split(':')[-1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.quote)
        else:
            print('Author not found.')

    elif query.startswith('tag:'):
        tag = query.split(':')[-1].strip()
        quotes = Quote.objects(tags__contains=tag)
        for quote in quotes:
            print(quote.quote)
        if quotes:
            for quote in quotes:
                print(quote.quote)
        else:
            print('No quotes found for the specified tag.')

    elif query.startswith('tags:'):
        tags = [t.strip() for t in query.split(':')[-1].split(',')]
        quotes = Quote.objects(tags__in=tags)
        for quote in quotes:
            print(quote.quote)

    elif query == 'exit':
        exit()

    else:
        print('Invalid command.')


if __name__ == "__main__":
    print("available search commands: tag:, tags:, name:, exit")
    while True:
        user_input = input('Enter command: ')
        search_quotes(user_input)
