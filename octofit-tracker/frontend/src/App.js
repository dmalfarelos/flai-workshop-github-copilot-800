import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import logo from './octofitapp-small.png';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navigation Bar */}
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand d-flex align-items-center" to="/">
              <img src={logo} alt="OctoFit Logo" className="navbar-logo me-2" />
              <strong>OctoFit Tracker</strong>
            </Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/users">Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">Workouts</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/users" element={<Users />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/workouts" element={<Workouts />} />
        </Routes>
      </div>
    </Router>
  );
}

// Home Page Component
function Home() {
  return (
    <div className="container mt-5">
      <div className="jumbotron text-center">
        <img src={logo} alt="OctoFit Logo" className="home-logo mb-4" />
        <h1 className="display-4">Welcome to OctoFit Tracker! 🏋️</h1>
        <p className="lead">Track your fitness activities, compete with your team, and achieve your goals!</p>
        <hr className="my-4" />
        <div className="row mt-5">
          <div className="col-md-4 mb-4">
            <div className="card shadow">
              <div className="card-body text-center">
                <h3>👥 Users</h3>
                <p>View all superhero team members</p>
                <Link to="/users" className="btn btn-primary">View Users</Link>
              </div>
            </div>
          </div>
          <div className="col-md-4 mb-4">
            <div className="card shadow">
              <div className="card-body text-center">
                <h3>🦸 Teams</h3>
                <p>Team Marvel vs Team DC</p>
                <Link to="/teams" className="btn btn-primary">View Teams</Link>
              </div>
            </div>
          </div>
          <div className="col-md-4 mb-4">
            <div className="card shadow">
              <div className="card-body text-center">
                <h3>🏃 Activities</h3>
                <p>Track all fitness activities</p>
                <Link to="/activities" className="btn btn-primary">View Activities</Link>
              </div>
            </div>
          </div>
          <div className="col-md-4 mb-4">
            <div className="card shadow">
              <div className="card-body text-center">
                <h3>🏆 Leaderboard</h3>
                <p>See who's leading the pack</p>
                <Link to="/leaderboard" className="btn btn-warning">View Leaderboard</Link>
              </div>
            </div>
          </div>
          <div className="col-md-4 mb-4">
            <div className="card shadow">
              <div className="card-body text-center">
                <h3>💪 Workouts</h3>
                <p>Get personalized workout suggestions</p>
                <Link to="/workouts" className="btn btn-success">View Workouts</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
