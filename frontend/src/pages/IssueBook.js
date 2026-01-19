import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const IssueBook = () => {
  const [books, setBooks] = useState([]);
  const [members, setMembers] = useState([]);
  const [formData, setFormData] = useState({
    book_id: '',
    member_id: '',
    due_date: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchBooksAndMembers();
  }, []);

  const fetchBooksAndMembers = async () => {
    try {
      const [booksRes, membersRes] = await Promise.all([
        api.get('/books/available/'),
        api.get('/members/'),
      ]);
      setBooks(booksRes.data);
      setMembers(membersRes.data.results || membersRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const payload = {
        book_id: parseInt(formData.book_id),
        member_id: parseInt(formData.member_id),
      };
      if (formData.due_date) {
        payload.due_date = formData.due_date;
      }

      await api.post('/issues/issue/', payload);
      setSuccess('Book issued successfully!');
      setFormData({ book_id: '', member_id: '', due_date: '' });
      fetchBooksAndMembers();
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (err) {
      const errorMessage =
        err.response?.data?.book_id?.[0] ||
        err.response?.data?.member_id?.[0] ||
        err.response?.data?.non_field_errors?.[0] ||
        'Failed to issue book';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Calculate default due date (14 days from now)
  const getDefaultDueDate = () => {
    const date = new Date();
    date.setDate(date.getDate() + 14);
    return date.toISOString().split('T')[0];
  };

  return (
    <div>
      <div className="page-header">
        <h1>Issue Book</h1>
      </div>

      <div className="form-container">
        <div className="card">
          {error && <div className="alert alert-error">{error}</div>}
          {success && <div className="alert alert-success">{success}</div>}
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Select Book</label>
              <select
                name="book_id"
                value={formData.book_id}
                onChange={handleChange}
                required
              >
                <option value="">-- Select a book --</option>
                {books.map((book) => (
                  <option key={book.id} value={book.id}>
                    {book.title} by {book.author} (Available: {book.available_copies})
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Select Member</label>
              <select
                name="member_id"
                value={formData.member_id}
                onChange={handleChange}
                required
              >
                <option value="">-- Select a member --</option>
                {members.map((member) => (
                  <option key={member.id} value={member.id}>
                    {member.user.first_name} {member.user.last_name} ({member.member_id})
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Due Date (Optional - Default: 14 days from today)</label>
              <input
                type="date"
                name="due_date"
                value={formData.due_date}
                onChange={handleChange}
                min={getDefaultDueDate()}
              />
            </div>

            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Issuing...' : 'Issue Book'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default IssueBook;
