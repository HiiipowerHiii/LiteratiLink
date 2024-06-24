import React, { useState, useEffect } from 'react';
import { fetchBooks, addBook, removeBook } from './api/books'; 

const BookList = ({ books: initialBooks }) => {
    const [bookList, setBookList] = useState(initialBooks); 
    const [fetchError, setFetchError] = useState(null);

    useEffect(() => {
        const loadBookList = async () => { 
            try {
                const fetchedBooks = await fetchBooks(); 
                setBookList(fetchedBooks);
            } catch (err) {
                setFetchError('Failed to fetch books. Please try again later.');
                console.error("Error fetching books:", err);
            }
        };
        
        loadBookList();
    }, []);

    const handleAddNewBook = async (newBook) => { 
        try {
            const updatedBookList = await addBook(newBook); 
            setBookList(updatedBookList);
        } catch (err) {
            setFetchError('Failed to add the book. Please try again later.'); 
            console.error("Error adding book:", err);
        }
    };

    const handleBookRemoval = async (bookId) => { 
        try {
            const reducedBookList = await removeBook(bookId); 
            setBookList(reducedBookList);
        } catch (err) {
            setFetchError('Failed to remove the book. Please try again later.'); 
            console.error("err removing book:", err);
        }
    };

    if (fetchError) {
        return <div>Error: {fetchError}</div>; 
    }

    return (
        <div>
            <ul>
                {bookList.map((bookItem) => ( 
                    <li key={bookItem.id}>
                        {bookItem.title} - <button onClick={() => handleBookRemoval(bookItem.id)}>Remove</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default BookList;