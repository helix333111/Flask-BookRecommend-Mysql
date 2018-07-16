from csv import DictReader

class bookDB():

    def __init__(self, books_csv):
        self._book_to_id = {}
        self._id_to_book = {}

        with open(books_csv, 'r') as f:
            reader = DictReader(f, delimiter=',')
            for row in reader:
                book_id = row['BookID']
                book = row['BookTitle']
                self._book_to_id[book] = book_id
                self._id_to_book[book_id] = book

    def book_to_id(self, book):
        return self._book_to_id[book]

    def id_to_book(self, book_id):
        return self._id_to_book[book_id]
