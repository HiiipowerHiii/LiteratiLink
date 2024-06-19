import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import BookList from './BookList';

const mockBooks = [
  { id: 1, title: "Book One", author: "Author One" },
  { id: 2, title: "Book Two", author: "Author Two" }
];

describe('BookList Component Tests', () => {
  it('should display a list of books', () => {
    render(<BookList books={mockBooks} />);
    const displayedBooks = screen.getAllByRole('listitem');
    expect(displayedBooks.length).toBe(mockBooks.length);
  });

  it('should add a new book when the form is submitted', async () => {
    render(<BookList books={mockBooks} />);
    const titleInput = screen.getByLabelText(/title/i);
    const authorInput = screen.getByLabelText(/author/i);
    const addButton = screen.getByRole('button', { name: /add book/i });

    fireEvent.change(titleInput, { target: { value: 'Book Three' } });
    fireEvent.change(authorInfoInput, { target: { value: 'Author Three' } });
    fireEvent.click(addButton);

    await waitFor(() => {
      const displayedBooks = screen.getAllByRole('listitem');
      expect(displayedBooks.length).toBe(mockBooks.length + 1);
    });
  });

  it('should remove a book when the remove button is clicked', async () => {
    render(<BookList books={[...mockBooks, { id: 3, title: "Book Three", author: "Author Three" }]} />);
    const removeButtons = screen.getAllByRole('button', { name: /remove/i });

    fireEvent.click(removeButtons[0]);

    await waitFor(() => {
      const displayedBooks = screen.getAllByRole('listitem');
      expect(displayedBooks.length).toBe(2);
    });
  });

  it('should update dynamically when new books are added', () => {
    const { rerender } = render(<BookList books={mockBooks} />);
    const newBookList = [...mockBooks, { id: 3, title: "Book Four", author: "Author Four" }];
    rerender(<BookList books={newBookList} />);
    const displayedBooks = screen.getAllByRole('listitem');
    expect(displayedBooks.length).toBe(3);
  });

});