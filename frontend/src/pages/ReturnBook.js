import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const ReturnBook = () => {
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [returning, setReturning] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchIssues();
  }, []);

  const fetchIssues = async () => {
    try {
      const response = await api.get('/issues/?status=issued');
      setIssues(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching issues:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReturn = async (issueId) => {
    if (!window.confirm('Are you sure you want to return this book?')) {
      return;
    }

    setError('');
    setSuccess('');
    setReturning(true);

    try {
      await api.post('/issues/return_book/', { issue_record_id: issueId });
      setSuccess('Book returned successfully!');
      fetchIssues();
    } catch (err) {
      const errorMessage =
        err.response?.data?.issue_record_id?.[0] ||
        err.response?.data?.non_field_errors?.[0] ||
        'Failed to return book';
      setError(errorMessage);
    } finally {
      setReturning(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading issued books...</div>;
  }

  return (
    <div>
      <div className="page-header">
        <h1>Return Book</h1>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div className="card">
        {issues.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Book</th>
                <th>Member</th>
                <th>Issue Date</th>
                <th>Due Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {issues.map((issue) => {
                const isOverdue =
                  new Date(issue.due_date) < new Date() && issue.status === 'issued';
                return (
                  <tr key={issue.id}>
                    <td>{issue.book.title}</td>
                    <td>
                      {issue.member.user.first_name} {issue.member.user.last_name} (
                      {issue.member.member_id})
                    </td>
                    <td>{new Date(issue.issue_date).toLocaleDateString()}</td>
                    <td>
                      {new Date(issue.due_date).toLocaleDateString()}
                      {isOverdue && (
                        <span className="badge badge-unavailable" style={{ marginLeft: '10px' }}>
                          Overdue
                        </span>
                      )}
                    </td>
                    <td>
                      <span
                        className={`badge ${
                          issue.status === 'issued'
                            ? 'badge-available'
                            : issue.status === 'overdue'
                            ? 'badge-unavailable'
                            : ''
                        }`}
                      >
                        {issue.status}
                      </span>
                    </td>
                    <td>
                      <button
                        onClick={() => handleReturn(issue.id)}
                        className="btn btn-success"
                        disabled={returning}
                      >
                        Return
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : (
          <p>No books currently issued</p>
        )}
      </div>
    </div>
  );
};

export default ReturnBook;
