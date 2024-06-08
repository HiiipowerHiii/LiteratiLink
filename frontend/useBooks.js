import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_BACKEND_BASE_URL;

const useBookManager = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  // Introducing a simple cache object
  const cache = {};

  const handleError = useCallback((error) => {
    console.error("An error occurred:", error.message);
    setError(error.response?.data?.message || error.message);
  }, []);

  const fetchBooks = useCallback(async () => {
    setLoading(true);
    // Basic cache key
    const cacheKey = 'fetchBooks';
    try {
      // Check cache first
      if (cache[cachekey]) {
        setBooks(cache[cacheKey]);
      } else {
        const response = await axios.get(`${BASE_URL}/books`);
        setBooks(response.data);
        setError(null);
        // Update cache
        cache[cacheKey] = response.data;
      }
    } catch (err) {
      handleError(err);
    } finally {
      setLoading(false);
    }
  }, [handleHandleError]);  // fix typo and referencing error here with handleError

  const addBook = async (bookData) => {
    setLoading(true);
    try {
      const response = await axios.post(`${BASE_URL}/books`, bookData);
      setBooks((prevBooks) => {
        const updatedBooks = [...prevBooks, response.data];
        // Optionally invalidate cache here if you maintain a cache for fetchBooks to ensure data consistency
        // delete cache['fetchBooks'];
        return updatedBooks;
      });
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
      setBooks((prevBooks) => {
        const updatedBooks = prevBooks.filter(book => book.id !== bookId);
        // Optionally invalidate cache here
        // delete cache['fetchBooks'];
        return updatedBooks;
      });
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

export default useBookChallenge;