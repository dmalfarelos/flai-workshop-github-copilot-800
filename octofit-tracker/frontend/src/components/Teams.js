import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const codespace = process.env.REACT_APP_CODESPACE_NAME;
        const baseUrl = codespace
          ? `https://${codespace}-8000.app.github.dev`
          : 'http://localhost:8000';
        const apiUrl = `${baseUrl}/api/teams/`;
        
        console.log('Fetching teams from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Teams data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        setTeams(Array.isArray(teamsData) ? teamsData : []);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching teams:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Teams</h2>
      <div className="row">
        {teams.map((team, index) => (
          <div key={team.id || index} className="col-md-6 mb-4">
            <div className="card h-100 shadow">
              <div className="card-header bg-primary text-white">
                <h4 className="mb-0">{team.name}</h4>
              </div>
              <div className="card-body">
                <p className="card-text">{team.description}</p>
                <hr />
                <p className="mb-2"><strong>Leader:</strong> <span className="badge bg-success">{team.leader}</span></p>
                <p className="mb-2"><strong>Total Points:</strong> <span className="badge bg-warning text-dark">{team.total_points}</span></p>
                <p className="mb-2"><strong>Members:</strong></p>
                <ul className="list-group">
                  {team.members && team.members.map((member, idx) => (
                    <li key={idx} className="list-group-item d-flex justify-content-between align-items-center">
                      {member}
                      {member === team.leader && <span className="badge bg-success">Leader</span>}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="card-footer text-muted">
                Created: {new Date(team.created_at).toLocaleDateString()}
              </div>
            </div>
          </div>
        ))}
      </div>
      {teams.length === 0 && (
        <div className="alert alert-info">No teams found.</div>
      )}
    </div>
  );
}

export default Teams;
