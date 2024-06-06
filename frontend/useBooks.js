import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_BACKEND_BASE_URL;

const useBookManager = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleError = useCallback((error) => {
    console.error("An error occurred:", error.message);
    setError(error.response?.data?.message || error.message);
  }, []);

  const fetchBooks = useCallback(async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${BASE_URL}/books`);
      setBooks(response.data);
      setError(null);  
    } catch (err) {
 device.     handleError(err);
    } finally {
      setLoading(false);
    }
  }, [handleError]);
  
  const addBook = async (bookData) => {
    setLoading(true);
    try {
      const response = await axios.post(`${BASE_URL}/books`, bookData);
      setBooks((prevBooks) => [...prevBooks, response.data]);
      setError(null);
    } catch (err) {
      handleError(err);
    } finally {
      setLoading(false);
    }
  };

  const removeBook = async (bookId) => {
    setLoading(true);
    try {
      await axios.delete(`${BASE_URL}/books/${bookId}`);
      setBooks((prevBooks) => prevBooks.filter(book => book.id !== bookId));
      setError(null);
    } catch (err) {
      handleError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, [fetchBooks]);

  return { books, loading, error, addBook, removeBook, fetchBooks, handleError };
};

export default useBookManager;