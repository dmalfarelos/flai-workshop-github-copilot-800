import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    team: '',
    role: '',
    avatar: ''
  });
  const [saveError, setSaveError] = useState(null);
  const [saving, setSaving] = useState(false);

  const getBaseUrl = () => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME;
    return codespace
      ? `https://${codespace}-8000.app.github.dev`
      : 'http://localhost:8000';
  };

  const fetchUsers = async () => {
    try {
      const baseUrl = getBaseUrl();
      const apiUrl = `${baseUrl}/api/users/`;
      
      console.log('Fetching users from:', apiUrl);
      
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Users data received:', data);
      
      // Handle both paginated (.results) and plain array responses
      const usersData = data.results || data;
      setUsers(Array.isArray(usersData) ? usersData : []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching users:', err);
      setError(err.message);
      setLoading(false);
    }
  };

  const fetchTeams = async () => {
    try {
      const baseUrl = getBaseUrl();
      const apiUrl = `${baseUrl}/api/teams/`;
      
      console.log('Fetching teams from:', apiUrl);
      
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Teams data received:', data);
      
      const teamsData = data.results || data;
      setTeams(Array.isArray(teamsData) ? teamsData : []);
    } catch (err) {
      console.error('Error fetching teams:', err);
    }
  };

  useEffect(() => {
    fetchUsers();
    fetchTeams();
  }, []);

  const handleEditClick = (user) => {
    setEditingUser(user);
    setFormData({
      name: user.name,
      email: user.email,
      team: user.team,
      role: user.role,
      avatar: user.avatar || ''
    });
    setSaveError(null);
    setShowEditModal(true);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSaveChanges = async () => {
    setSaving(true);
    setSaveError(null);

    try {
      const baseUrl = getBaseUrl();
      const apiUrl = `${baseUrl}/api/users/${editingUser.id}/`;
      
      console.log('Updating user:', apiUrl, formData);
      
      const response = await fetch(apiUrl, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      console.log('User updated successfully');
      
      // Refresh users list
      await fetchUsers();
      
      // Close modal
      setShowEditModal(false);
      setEditingUser(null);
    } catch (err) {
      console.error('Error updating user:', err);
      setSaveError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleCloseModal = () => {
    setShowEditModal(false);
    setEditingUser(null);
    setSaveError(null);
  };

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <>
      <div className="container mt-4">
        <h2 className="mb-4">Users</h2>
        <div className="row">
          {users.map((user, index) => (
            <div key={user.id || index} className="col-md-4 mb-4">
              <div className="card text-center shadow-sm">
                <div className="card-body">
                  <div className="mb-3">
                    <div className="rounded-circle bg-primary text-white d-inline-flex align-items-center justify-content-center" 
                         style={{width: '80px', height: '80px', fontSize: '2rem'}}>
                      {user.name.charAt(0)}
                    </div>
                  </div>
                  <h5 className="card-title">{user.name}</h5>
                  <p className="text-muted mb-2">{user.email}</p>
                  <div className="mb-2">
                    <span className="badge bg-info">{user.team}</span>
                  </div>
                  <div className="mb-2">
                    {user.role === 'team_lead' ? (
                      <span className="badge bg-warning text-dark">Team Leader</span>
                    ) : (
                      <span className="badge bg-secondary">Member</span>
                    )}
                  </div>
                  <button 
                    className="btn btn-sm btn-primary mt-2"
                    onClick={() => handleEditClick(user)}
                  >
                    ✏️ Edit
                  </button>
                </div>
                <div className="card-footer text-muted">
                  <small>Joined: {new Date(user.created_at).toLocaleDateString()}</small>
                </div>
              </div>
            </div>
          ))}
        </div>
        {users.length === 0 && (
          <div className="alert alert-info">No users found.</div>
        )}
      </div>

      {/* Edit User Modal */}
      {showEditModal && (
        <div className="modal show d-block" tabIndex="-1" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Edit User Details</h5>
                <button type="button" className="btn-close" onClick={handleCloseModal}></button>
              </div>
              <div className="modal-body">
                {saveError && (
                  <div className="alert alert-danger">{saveError}</div>
                )}
                <form>
                  <div className="mb-3">
                    <label htmlFor="name" className="form-label">Name</label>
                    <input
                      type="text"
                      className="form-control"
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-control"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="team" className="form-label">Team</label>
                    <select
                      className="form-select"
                      id="team"
                      name="team"
                      value={formData.team}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="">Select Team...</option>
                      {teams.map((team, index) => (
                        <option key={team.id || index} value={team.name}>
                          {team.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="mb-3">
                    <label htmlFor="role" className="form-label">Role</label>
                    <select
                      className="form-select"
                      id="role"
                      name="role"
                      value={formData.role}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="">Select Role...</option>
                      <option value="member">Member</option>
                      <option value="team_lead">Team Leader</option>
                    </select>
                  </div>
                  <div className="mb-3">
                    <label htmlFor="avatar" className="form-label">Avatar URL (optional)</label>
                    <input
                      type="text"
                      className="form-control"
                      id="avatar"
                      name="avatar"
                      value={formData.avatar}
                      onChange={handleInputChange}
                      placeholder="https://..."
                    />
                  </div>
                </form>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={handleCloseModal}>
                  Cancel
                </button>
                <button 
                  type="button" 
                  className="btn btn-primary" 
                  onClick={handleSaveChanges}
                  disabled={saving}
                >
                  {saving ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Saving...
                    </>
                  ) : (
                    'Save Changes'
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Users;
