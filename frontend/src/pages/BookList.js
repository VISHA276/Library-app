import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const BookList = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchBooks();
  }, [searchTerm]);

  const fetchBooks = async () => {
    try {
      setLoading(true);
      const params = searchTerm ? { search: searchTerm } : {};
      const response = await api.get('/books/', { params });
      setBooks(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching books:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading books...</div>;
  }

  return (
    <div>
      <div className="page-header">
        <h1>Books</h1>
      </div>

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search books by title, author, or ISBN..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="book-grid">
        {books.length > 0 ? (
          books.map((book) => (
            <div key={book.id} className="book-card">
              <h3>{book.title}</h3>
              <p>
                <strong>Author:</strong> {book.author}
              </p>
              <p>
                <strong>ISBN:</strong> {book.isbn}
              </p>
              <p>
                <strong>Available:</strong> {book.available_copies} / {book.total_copies}
              </p>
              {book.available_copies > 0 ? (
                <span className="badge badge-available">Available</span>
              ) : (
                <span className="badge badge-unavailable">Unavailable</span>
              )}
              <div style={{ marginTop: '15px' }}>
                <Link to={`/books/${book.id}`} className="btn btn-primary">
                  View Details
                </Link>
              </div>
            </div>
          ))
        ) : (
          <p>No books found</p>
        )}
      </div>
    </div>
  );
};

export default BookList;
