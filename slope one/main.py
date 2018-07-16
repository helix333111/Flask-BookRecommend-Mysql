from collections import defaultdict
from csv import DictReader
import re
from sys import float_info
from model import SlopeOne
from bookdb import bookDB
EPS = float_info.epsilon


def get_ratings(book_db):
    user_ratings = {}
    print('Please enter your ratings in a "book, rating" format.')
    print("The rating should be a number from 0.5 to 5.")
    print("Press ENTER on an empty line to end input.")
    while True:
        line = input().strip()
        if line == '':
            break
        try:
            book_id, rating = parse_rating(line, book_db)
        except ValueError:
            continue
        else:
            user_ratings[book_id] = rating
    return user_ratings


def parse_rating(rating_string, book_db):
    regex = re.compile(r'^(.*?)\s*,\s*([0-9]*\.[0-9]+|[0-9]+)$')
    result = regex.match(rating_string)
    if not result:
        print('Line should be a rating in the format "book (year), rating". For example')
        print('Peter Pan (1953), 4.5')
        raise ValueError()

    book_name = result.group(1)
    try:
        book_id = book_db.book_to_id(book_name)
    except KeyError:
        print("Can't find the book \"{}\". Please check books.csv for exact spelling.".format(book_name))
        raise ValueError("Cannot find book \"{}\".".format(book_name))
    rating = float(result.group(2))
    if rating - 5.0 > EPS or rating - 0.5 < EPS:
        print("Rating should be between 0.5 and 5.0.")
        raise ValueError("Rating should be between 0.5 and 5.0.")
    return (book_id, rating)


def print_books(book_ids, book_db):
    for book_id in book_ids:
        try:
            book_name = book_db.id_to_book(book_id)
        except KeyError:
            continue
        else:
            print(book_name)


def read_ratings(filename):
    with open(filename, 'r',encoding='utf-8') as f:
        reader = DictReader(f, delimiter=',')
        users = defaultdict(dict)

        for row in reader:
            print(row)
            user_id = row['UserID']
            book_id = row['BookID']
            rating = int(row['Rating'])
            users[user_id][book_id] = rating
        return users


def main():
    print("Training model. This might take a while...\n")

    recommender = SlopeOne()
    users_dict = read_ratings('ml/bookrating.csv')
    recommender.train(users_dict)
    book_db = bookDB('ml/book.csv')

    user_ratings = get_ratings(book_db)
    book_ids = recommender.get_recommendations(user_ratings)
    print("My recommendations for you are: ")
    print_books(book_ids, book_db)


if __name__ == '__main__':
    main()
