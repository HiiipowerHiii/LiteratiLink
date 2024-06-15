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
            self.fail(f"setUp failed to add sample book: {e}")  # Enhanced to use self.fail for setup issues.

    def test_addBook_success(self):
        bookCountBeforeAdding = len(self.bookManager.books)
        newBookDetails = {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "isbn": "978-0132350884"
        }
        self.bookManager.add_book(newBookDetails)  # Assuming this should not raise under normal conditions.
        self.assertEqual(len(self.bookManager.books), bookCountBeforeAdding + 1)

    def test_removeBookByISBN_bookRemoved(self):
        self.bookManager.remove_book_by_isbn(self.sampleBook["isbn"])  # Assuming this should not raise under normal conditions.

        with self.assertRaises(BookNotFoundError):
            self.bookManager.get_book_by_isbn(self.sampleBook["isbn"])

    def test_updateBookTitle_titleUpdated(self):
        updatedTitle = "Pragmatic Programmer, The: Your Journey to Mastery"
        self.bookManager.update_book(self.sampleBook["isbn"], 'title', updatedTitle)  # Assuming this should not raise under normal conditions.
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
        self.assertIsNotNone(databaseHost)  # No need for try-except here as getenv and assertIsNotNone should not raise.

    @patch('book_manager.BookManager._send_update_notification')
    def test_notificationOnBookUpdate_notificationSent(self, mockUpdateNotification):
        self.bookManager.update_book(self.sampleBook["isbn"], 'title', "Updated Title")
        mockUpdateNotification.assert_called_once()

    def tearDown(self):
        self.bookManager.books.clear()  # Assuming this clear operation is straightforward and should not fail under normal conditions.

if __name__ == '__main__':
    unittest.main()