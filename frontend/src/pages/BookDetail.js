import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';

const BookDetail = () => {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchBook();
  }, [id]);

  const fetchBook = async () => {
    try {
      const response = await api.get(`/books/${id}/`);
      setBook(response.data);
    } catch (error) {
      setError('Book not found');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading book details...</div>;
  }

  if (error || !book) {
    return (
      <div>
        <div className="alert alert-error">{error || 'Book not found'}</div>
        <Link to="/books" className="btn btn-secondary">
          Back to Books
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <Link to="/books" className="btn btn-secondary" style={{ marginBottom: '20px' }}>
          ← Back to Books
        </Link>
        <h1>{book.title}</h1>
      </div>

      <div className="card">
        <h2>Book Details</h2>
        <table className="table">
          <tbody>
            <tr>
              <td><strong>Title</strong></td>
              <td>{book.title}</td>
            </tr>
            <tr>
              <td><strong>Author</strong></td>
              <td>{book.author}</td>
            </tr>
            <tr>
              <td><strong>ISBN</strong></td>
              <td>{book.isbn}</td>
            </tr>
            <tr>
              <td><strong>Publication Date</strong></td>
              <td>
                {book.publication_date
                  ? new Date(book.publication_date).toLocaleDateString()
                  : 'N/A'}
              </td>
            </tr>
            <tr>
              <td><strong>Total Copies</strong></td>
              <td>{book.total_copies}</td>
            </tr>
            <tr>
              <td><strong>Available Copies</strong></td>
              <td>{book.available_copies}</td>
            </tr>
            <tr>
              <td><strong>Status</strong></td>
              <td>
                {book.available_copies > 0 ? (
                  <span className="badge badge-available">Available</span>
                ) : (
                  <span className="badge badge-unavailable">Unavailable</span>
                )}
              </td>
            </tr>
            {book.description && (
              <tr>
                <td><strong>Description</strong></td>
                <td>{book.description}</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {book.available_copies > 0 && (
        <div style={{ marginTop: '20px' }}>
          <Link to="/issue" className="btn btn-success">
            Issue This Book
          </Link>
        </div>
      )}
    </div>
  );
};

export default BookDetail;
