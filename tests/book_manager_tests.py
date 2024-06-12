import unittest
from unittest.mock import patch
from book_manager import BookManager, BookNotFoundError
import os
from dotenv import load_dotenv

load_dotenv()

class TestBookManager(unittest.TestCase):
    def setUp(self):
        self.bookManager = BookManager()
        self.sampleBook = {
            "title": "The Pragmatic Programmer",
            "author": "Andy Hunt",
            "isbn": "978-0201616224"
        }
        self.bookManager.add_book(self.sampleBook)

    def test_addBook_success(self):
        bookCountBeforeAdding = len(self.bookManager.books)
        newBookDetails = {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "isbn": "978-0132350884"
        }
        self.bookManager.add_book(newBookDetails)
        self.assertEqual(len(self.bookManager.books), bookCountBeforeAdding + 1)

    def test_removeBookByISBN_bookRemoved(self):
        self.bookManager.remove_book_by_isbn(self.sampleBook["isbn"])
        with self.assertRaises(BookNotFoundError):
            self.bookManager.get_book_by_isbn(self.sampleBook["isbn"])

    def test_updateBookTitle_titleUpdated(self):
        updatedTitle = "Pragmatic Programmer, The: Your Journey to Mastery"
        self.bookManager.update_book(self.sampleBook["isbn"], 'title', updatedTitle)
        updatedBook = self.bookManager.get_book_by_isbn(self.sampleBook["isbn"])
        self.assertEqual(updatedBook["title"], updatedTitle)

    def test_getBookByISBN_bookFound(self):
        retrievedBook = self.bookManager.get_book_by_isbn(self.sampleBook["isbn"])
        self.assertDictEqual(retrievedBook, self.sampleBook)

    def test_searchForNonexistentBook_raisesBookNotFoundError(self):
        with self.assertRaises(BookNotFoundError):
            self.bookManager.get_book_by_isbn("non-existent-isbn")

    def test_databaseHostEnvironmentVariable_notNone(self):
        databaseHost = os.getenv("DB_HOST")
        self.assertIsNotNone(databaseHost)

    @patch('book_manager.BookManager._send_update_notification')
    def test_notificationOnBookUpdate_notificationSent(self, mockUpdateNotification):
        self.bookManager.update_book(self.sampleBook["isbn"], 'title', "Updated Title")
        mockUpdateNotification.assert_called_once()

    def tearDown(self):
        self.bookManager.books.clear()

if __name__ == '__main__':
    unittest.main()