import os
import requests
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
OPEN_LIBRARY_API_URL = "https://openlibrary.org/api/books"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class Book:
    def __init__(self, title, author, isbn, user_id):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.user_id = user_id

    def __str__(self):
        return f"{self.title} by {self.author}"

class BookManager:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, isbn, user_id):
        new_book = Book(title, author, isbn, user_id)
        self.books.append(new_book)
        return new_book

    def remove_book(self, isbn):
        self.books = [book for book in self.books if book.isbn != isbn]

    def find_book(self, isbn):
        return next((book for book in self.books if book.isbn == isbn), None)

    def list_books(self, user_id):
        return [book for book in self.books if book.user_id == user_id]

    @lru_cache(maxsize=128)
    def fetch_book_metadata(self, isbn, source="google"):
        if source == "google":
            params = {"q": f"isbn:{isbn}", "key": GOOGLE_API_KEY}
            response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        else:
            url = f"{OPEN_LIBRARY_API_URL}?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
            response = requests.get(url)

        return response.json() if response.status_code == 200 else {}

if __name__ == "__main__":
    book_manager = BookManager()
    print("Adding book...")
    book = book_manager.add_book("Pride and Prejudice", "Jane Austen", "1234567890", 1)

    print("Fetching metadata from Google Books...")
    metadata_google = book_manager.fetch_book_metadata(book.isbn, "google")
    print(metadata_google)

    print("Fetching metadata from Open Library...")
    metadata_openlibrary = book_manager.fetch_book_metadata(book.isbn, "openlibrary")
    print(metadata_openlibrary)