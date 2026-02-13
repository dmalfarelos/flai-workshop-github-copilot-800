import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        const codespace = process.env.REACT_APP_CODESPACE_NAME;
        const baseUrl = codespace
          ? `https://${codespace}-8000.app.github.dev`
          : 'http://localhost:8000';
        const apiUrl = `${baseUrl}/api/workouts/`;
        
        console.log('Fetching workouts from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Workouts data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching workouts:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  const getDifficultyBadge = (difficulty) => {
    const badges = {
      'beginner': 'bg-success',
      'intermediate': 'bg-warning text-dark',
      'advanced': 'bg-danger'
    };
    return badges[difficulty] || 'bg-secondary';
  };

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Workout Suggestions</h2>
      <div className="row">
        {workouts.map((workout, index) => (
          <div key={workout.id || index} className="col-md-6 mb-4">
            <div className="card h-100 shadow">
              <div className="card-header bg-dark text-white">
                <h4 className="mb-0">{workout.name}</h4>
                <span className={`badge ${getDifficultyBadge(workout.difficulty)}`}>
                  {workout.difficulty}
                </span>
                <span className="badge bg-info ms-2">{workout.category}</span>
              </div>
              <div className="card-body">
                <p className="card-text">{workout.description}</p>
                <hr />
                <p className="mb-2">
                  <strong>Duration:</strong> {workout.duration_minutes} minutes
                </p>
                <p className="mb-2"><strong>Exercises:</strong></p>
                <ul className="list-group mb-3">
                  {workout.exercises && workout.exercises.map((exercise, idx) => (
                    <li key={idx} className="list-group-item">{exercise}</li>
                  ))}
                </ul>
                <p className="mb-2"><strong>Target Muscles:</strong></p>
                <div className="mb-3">
                  {workout.target_muscles && workout.target_muscles.map((muscle, idx) => (
                    <span key={idx} className="badge bg-secondary me-1">{muscle}</span>
                  ))}
                </div>
                <p className="mb-2"><strong>Recommended For:</strong></p>
                <div>
                  {workout.recommended_for && workout.recommended_for.map((level, idx) => (
                    <span key={idx} className="badge bg-primary me-1">{level}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      {workouts.length === 0 && (
        <div className="alert alert-info">No workouts found.</div>
      )}
    </div>
  );
}

export default Workouts;
