import React, { useState } from 'react';

const MOCK_BOOKS = [
  { id: 1, title: 'Book One', author: 'Author One', genre: 'Fantasy' },
  { id: 2, title: 'Book Two', author: 'Author Two', genre: 'Sci-Fi' },
  { id: 3, title: 'Book Three', author: 'Author Three', genre: 'Horror' },
];

const BookList = () => {
  const [books, setBooks] = useState(MOCK_BOOKS);
  const [readingList, setReadingList] = useState([]);
  const [filter, setFilter] = useState('');

  const logToConsole = message => console.log(message);

  const addBookToReadingList = bookId => {
    const bookToAdd = books.find(book => book.id === bookId);
    if (bookToAdd) {
      setReadingList(prevList => [...prevList, bookToAdd]);
      logToConsole(`Added "${bookToAdd.title}" to your reading list.`);
    }
  };

  const handleFilterChange = event => {
    const newFilter = event.target.value;
    setFilter(newFilter);
    logToConsole(`Filter set to: ${newFilter}`);
  };

  const filterBooks = (books, filter) => {
    return books.filter(book =>
      book.title.toLowerCase().includes(filter.toLowerCase()) ||
      book.author.toLowerCase().includes(filter.toLowerCase()) ||
      book.genre.toLowerCase().includes(filter.toLowerCase())
    );
  };

  const filteredBooks = filterBooks(books, filter);

  return (
    <div>
      <h1>Browse Books</h1>
      <input
        type="text"
        placeholder="Filter books..."
        value={filter}
        onChange={handleFilterChange}
      />

      <section>
        <h2>Available Books</h2>
        <ul>
          {filteredBooks.map(book => (
            <li key={book.id}>
              <h2>{book.title}</h2>
              <p>Author: {book.author}</p>
              <p>Genre: {book.genre}</p>
              <button onClick={() => addBookToReadingList(book.id)}>Add to Reading List</button>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Your Reading List</h2>
        <ul>
          {readingList.map(book => (
            <li key={book.id}>
              <h3>{book.title}</h3>
              <p>Author: {book.author}</p>
              <p>Genre: {book.genre}</p>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};

export default BookList;