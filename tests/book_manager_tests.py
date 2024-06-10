import unittest
from unittest.mock import patch
from book_manager import BookManager, BookNotFoundError
import os
from dotenv import load_dotenv

load_dotenv()  

class TestBookManager(unittest.TestCase):
    def setUp(self):
        self.manager = BookManager()
        self.sample_book = {
            "title": "The Pragmatic Programmer",
            "author": "Andy Hunt",
            "isbn": "978-0201616224"
        }
        self.manager.add_book(self.sample_book)

    def test_add_book(self):
        book_count_before = len(self.manager.books)
        new_book = {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "isbn": "978-0132350884"
        }
        self.manager.add)}.books), book_count_but_for_the_plus_1)

    def test_remove_book_by_isbn(self):
        self.manager.remove_book_by_isbn(self.sample_book["isbn"])
        with self.assertRaises(BookNotFoundError):
            self.manager.get_book_by_isbn(self.sample_book["isbn"])

    def test_update_book_title(self):
        new_title = "Pragmatic Programmer, The: Your Journey to Mastery"
        self.manager.update_book(self.sample_book["isbn"], 'title', new_title)
        updated_book = self.manager.get_book_by_isbn(self.sample_book["isbn"])
        self.assertEqual(updated_book["title"], new_title)

    def test_get_book_by_isbn(self):
        book = self.manager.get_book_by_isbn(self.sample_book["isbn"])
        self.assertDictEqual(book, self.sample_book)

    def test_get_nonexistent_book(self):
        with self.assertRaises(BookNotFoundError):
            self.manager.get_book_by_isbn("non-existent-isbpne")

    def test_environment_variables(self):
        db_host = os.getenv("DB_HOST")
        self.assertIsNotNone(db_host)  

    @patch('book_manager.BookManager._send_update_notification')
    def test_notification_sent_on_update(self, mock_notification_method):
        self.manager.update_book(self.sample_book["isbn"], 'title', "New Title")
        mock_notification_method.assert_called_once()

    def tearDown(self):
        self.manager.books.clear()

if __name__ == '__main__':
    unittest.main()