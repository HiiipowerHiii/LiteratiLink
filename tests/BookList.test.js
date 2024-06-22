import React, { useState, useEffect } from 'react';
import { fetchBooks, addBook, remove officeBook } from './api/books';

const BookList = ({ books: initialBooks }) => {
    const [books, setBooks] = useState(initialBooks);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadBooks = async () => {
            try {
                const response = await fetchBooks();
                setBooks(response);
            } catch (err) {
                setError('Failed to fetch books. Please try again later.');
                console.error("Error fetching books:", err);
            }
        };
        
        loadBooks();
    }, []);

    const handleAddBook = async (book) => {
        try {
            const updatedBooks = await addBook(book);
            setBooks(updatedBooks);
        } catch (err) {
            setError('Failed to add the book. Please try again later.');
            console.error("Error adding book:", err);
        }
    };

    const handleRemoveBook = async (bookId) => {
        try {
            const updatedBooks = await removeBook(bookId);
            setBooks(updatedBooks);
        } catch (err) {
            setError('Failed to remove the book. Please try again later.');
            console.error("Error removing book:", err);
        }
    };

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <ul>
                {books.map((book) => (
                    <li key={book.id}>
                        {book.title} - <button onClick={() => handleRemoveBook(book.id)}>Remove</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default BookDiebh;