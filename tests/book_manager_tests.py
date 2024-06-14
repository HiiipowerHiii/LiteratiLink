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
        try:
            self.bookManager.add_book(self.sampleBook)
        except Exception as e:
            print(f"Failed to add sample book: {e}")

    def test_addBook_success(self):
        try:
            bookCountBeforeAdding = len(self.bookManager.books)
            newBookDetails = {
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "isbn": "978-0132350884"
            }
            self.bookManager.add_book(newBookDetails)
            self.assertEqual(len(self.bookManager.books), bookCountBeforeAdding + 1)
        except Exception as e:
            self.fail(f"Adding a book failed with an exception: {e}")

    def test_removeBookByISBN_bookRemoved(self):
        try:
            self.bookManager.remove_book_by_isbn(self.sampleBook["isbn"])
        except BookNotFoundError:
            self.fail("BookNotFoundError raised unexpectedly when trying to remove a book by ISBN.")
        except Exception as e:
            self.fail(f"Removing a book failed with an unexpected exception: {e}")

        with self.assertRaises(BookNotFoundError):
            self.bookManager.get_book_by_isbn(self.sampleBook["isbn"])

    def test_updateBookTitle_titleUpdated(self):
        try:
            updatedTitle = "Pragmatic Programmer, The: Your Journey to Mastery"
            self.bookManager.update_book(self.sampleBook["isbn"], 'title', updatedTitle)
            updatedBook = self.bookManager.get_book_by_isbn(self.sampleBook["isbn"])
            self.assertEqual(updatedBook["title"], updatedTitle)
        except Exception as e:
            self.fail(f"Updating book title failed with an exception: {e}")

    def test_getBookByISBN_bookFound(self):
        try:
            retrievedBook = self.bookManager.get_book_by_isbn(self.sampleBook["isbn"])
            self.assertDictEqual(retrievedBook, self.sampleBook)
        except Exception as e:
            self.fail(f"Retrieving book by ISBN failed with an exception: {e}")

    def test_searchForNonexistentBook_raisesBookNotFoundError(self):
        with self.assertRaises(BookNotFoundError):
            self.bookManager.get_book_by_isbn("non-existent-isbn")

    def test_databaseHostEnvironmentVariable_notNone(self):
        try:
            databaseHost = os.getenv("DB_HOST")
            self.assertIsNotNone(databaseHost)
        except Exception as e:
            self.fail(f"Retrieving 'DB_HOST' environment variable failed with an exception: {e}")

    @patch('book_manager.BookManager._send_update_notification')
    def test_notificationOnBookUpdate_notificationSent(self, mockUpdateNotification):
        try:
            self.bookManager.update_book(self.sampleBook["isbn"], 'title', "Updated Title")
            mockUpdateNotification.assert_called_once()
        except Exception as e:
            self.fail(f"Notification sending on book update failed with an exception: {e}")

    def tearDown(self):
        try:
            self.bookManager.books.clear()
        except Exception as e:
            print(f"Failed to clear books in tearDown: {e}")

if __name__ == '__main__':
    unittest.main()