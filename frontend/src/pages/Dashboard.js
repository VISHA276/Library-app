import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalBooks: 0,
    availableBooks: 0,
    totalMembers: 0,
    issuedBooks: 0,
  });
  const [loading, setLoading] = useState(true);
  const [recentIssues, setRecentIssues] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [booksRes, availableRes, membersRes, issuesRes] = await Promise.all([
        api.get('/books/'),
        api.get('/books/available/'),
        api.get('/members/'),
        api.get('/issues/?status=issued'),
      ]);

      setStats({
        totalBooks: booksRes.data.count || booksRes.data.length,
        availableBooks: availableRes.data.length,
        totalMembers: membersRes.data.count || membersRes.data.length,
        issuedBooks: issuesRes.data.count || issuesRes.data.length,
      });

      // Get recent issues
      const recent = issuesRes.data.slice(0, 5);
      setRecentIssues(recent);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div>
      <div className="page-header">
        <h1>Dashboard</h1>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>{stats.totalBooks}</h3>
          <p>Total Books</p>
        </div>
        <div className="stat-card">
          <h3>{stats.availableBooks}</h3>
          <p>Available Books</p>
        </div>
        <div className="stat-card">
          <h3>{stats.totalMembers}</h3>
          <p>Total Members</p>
        </div>
        <div className="stat-card">
          <h3>{stats.issuedBooks}</h3>
          <p>Issued Books</p>
        </div>
      </div>

      <div className="card">
        <h2>Recent Issues</h2>
        {recentIssues.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Book</th>
                <th>Member</th>
                <th>Issue Date</th>
                <th>Due Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {recentIssues.map((issue) => (
                <tr key={issue.id}>
                  <td>{issue.book.title}</td>
                  <td>
                    {issue.member.user.first_name} {issue.member.user.last_name}
                  </td>
                  <td>{new Date(issue.issue_date).toLocaleDateString()}</td>
                  <td>{new Date(issue.due_date).toLocaleDateString()}</td>
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
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No recent issues</p>
        )}
      </div>

      <div style={{ marginTop: '20px' }}>
        <Link to="/books" className="btn btn-primary">
          View All Books
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;
