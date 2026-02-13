import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const codespace = process.env.REACT_APP_CODESPACE_NAME;
        const baseUrl = codespace
          ? `https://${codespace}-8000.app.github.dev`
          : 'http://localhost:8000';
        const apiUrl = `${baseUrl}/api/leaderboard/`;
        
        console.log('Fetching leaderboard from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Leaderboard data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching leaderboard:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Leaderboard</h2>
      <div className="row">
        <div className="col-md-8 offset-md-2">
          <div className="card">
            <div className="card-header bg-warning text-dark">
              <h4 className="mb-0">Top Performers</h4>
            </div>
            <div className="card-body p-0">
              <table className="table table-hover mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Rank</th>
                    <th>User</th>
                    <th>Team</th>
                    <th>Points</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((entry, index) => (
                    <tr key={entry.id || index} className={index < 3 ? 'table-success' : ''}>
                      <td>
                        {entry.rank === 1 && <span className="badge bg-warning text-dark">🥇 1st</span>}
                        {entry.rank === 2 && <span className="badge bg-secondary">🥈 2nd</span>}
                        {entry.rank === 3 && <span className="badge bg-danger">🥉 3rd</span>}
                        {entry.rank > 3 && <strong>{entry.rank}</strong>}
                      </td>
                      <td><strong>{entry.user_name}</strong></td>
                      <td><span className="badge bg-info">{entry.team}</span></td>
                      <td><strong className="text-success">{entry.total_points}</strong> pts</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      {leaderboard.length === 0 && (
        <div className="alert alert-info mt-3">No leaderboard data found.</div>
      )}
    </div>
  );
}

export default Leaderboard;
