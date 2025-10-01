import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { isAuthenticated, removeToken } from '../utils/auth';
import { updateUser, checkUsername, getUserProfile } from '../utils/api';

function Profile() {
  const navigate = useNavigate();
  
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [username, setUsername] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [profilePic, setProfilePic] = useState('');
  const [email, setEmail] = useState('');
  
  // Editing state
  const [editUsername, setEditUsername] = useState('');
  const [editDisplayName, setEditDisplayName] = useState('');
  const [editProfilePic, setEditProfilePic] = useState('');
  
  const [usernameAvailable, setUsernameAvailable] = useState<boolean | null>(null);
  const [usernameCheckLoading, setUsernameCheckLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    // Check authentication
    if (!isAuthenticated()) {
      navigate('/login');
      return;
    }

    // Load user data from API
    const loadUserProfile = async () => {
      try {
        setIsLoading(true);
        const profile = await getUserProfile();
        setEmail(profile.email);
        setUsername(profile.username);
        setDisplayName(profile.display_name);
        setProfilePic(profile.profile_pic);
      } catch (error) {
        console.error('Failed to load profile:', error);
        // If we get an error (like 401), the axios interceptor will redirect to login
      } finally {
        setIsLoading(false);
      }
    };

    loadUserProfile();
  }, [navigate]);

  // Check username availability when editing
  useEffect(() => {
    if (!isEditing || !editUsername || editUsername.length < 3) {
      setUsernameAvailable(null);
      return;
    }

    // Don't check if username hasn't changed
    if (editUsername === username) {
      setUsernameAvailable(true);
      return;
    }

    const timeoutId = setTimeout(async () => {
      setUsernameCheckLoading(true);
      try {
        const available = await checkUsername(editUsername);
        setUsernameAvailable(available);
      } catch (err) {
        console.error('Failed to check username:', err);
      } finally {
        setUsernameCheckLoading(false);
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [editUsername, username, isEditing]);

  const handleEdit = () => {
    setEditUsername(username);
    setEditDisplayName(displayName);
    setEditProfilePic(profilePic);
    setIsEditing(true);
    setError('');
    setSuccessMessage('');
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditUsername('');
    setEditDisplayName('');
    setEditProfilePic('');
    setError('');
    setUsernameAvailable(null);
  };

  const handleSave = async () => {
    setError('');
    setSuccessMessage('');

    // Validation
    if (editUsername && editUsername.length < 3) {
      setError('Username must be at least 3 characters long');
      return;
    }

    if (!editDisplayName || editDisplayName.length < 1) {
      setError('Display name is required');
      return;
    }

    if (editUsername !== username && usernameAvailable === false) {
      setError('Username is already taken');
      return;
    }

    setIsSubmitting(true);

    try {
      const updateData: any = {};
      
      if (editUsername && editUsername !== username) {
        updateData.username = editUsername;
      }
      if (editDisplayName !== displayName) {
        updateData.display_name = editDisplayName;
      }
      if (editProfilePic !== profilePic) {
        updateData.profile_pic = editProfilePic;
      }

      if (Object.keys(updateData).length === 0) {
        setError('No changes to save');
        setIsSubmitting(false);
        return;
      }

      await updateUser(updateData);
      
      // Update local state
      if (updateData.username) setUsername(updateData.username);
      if (updateData.display_name) setDisplayName(updateData.display_name);
      if (updateData.profile_pic) setProfilePic(updateData.profile_pic);
      
      setIsEditing(false);
      setSuccessMessage('Profile updated successfully!');
    } catch (err: any) {
      console.error('Update failed:', err);
      setError(err.response?.data?.error || 'Failed to update profile. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLogout = () => {
    removeToken();
    navigate('/login');
  };

  return (
    <div className="profile-container">
      <div className="profile-card">
        <div className="profile-header">
          <h1>My Profile</h1>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>

        {successMessage && <div className="success-message">{successMessage}</div>}
        {error && <div className="error-message">{error}</div>}

        {isLoading ? (
          <div className="profile-content">
            <p>Loading profile...</p>
          </div>
        ) : (
          <div className="profile-content">
          <div className="profile-pic-section">
            <img 
              src={isEditing ? editProfilePic || profilePic : profilePic} 
              alt="Profile" 
              className="profile-pic-large"
              onError={(e) => {
                e.currentTarget.src = 'https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg';
              }}
            />
          </div>

          {!isEditing ? (
            <div className="profile-info">
              <div className="info-item">
                <label>Username</label>
                <p>@{username}</p>
              </div>

              <div className="info-item">
                <label>Email</label>
                <p>{email}</p>
              </div>

              <div className="info-item">
                <label>Display Name</label>
                <p>{displayName}</p>
              </div>

              <button onClick={handleEdit} className="edit-btn">
                Edit Profile
              </button>
            </div>
          ) : (
            <div className="profile-edit-form">
              <div className="form-group">
                <label htmlFor="editDisplayName">Display Name *</label>
                <input
                  id="editDisplayName"
                  type="text"
                  value={editDisplayName}
                  onChange={(e) => setEditDisplayName(e.target.value)}
                  placeholder="Your full name"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="editUsername">Username</label>
                <input
                  id="editUsername"
                  type="text"
                  value={editUsername}
                  onChange={(e) => setEditUsername(e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, ''))}
                  placeholder="Choose a unique username"
                  minLength={3}
                />
                {editUsername && editUsername.length >= 3 && editUsername !== username && (
                  <div className="username-feedback">
                    {usernameCheckLoading ? (
                      <span className="checking">Checking availability...</span>
                    ) : usernameAvailable === true ? (
                      <span className="available">✓ Username is available</span>
                    ) : usernameAvailable === false ? (
                      <span className="unavailable">✗ Username is taken</span>
                    ) : null}
                  </div>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="editProfilePic">Profile Picture URL</label>
                <input
                  id="editProfilePic"
                  type="url"
                  value={editProfilePic}
                  onChange={(e) => setEditProfilePic(e.target.value)}
                  placeholder="https://example.com/your-photo.jpg"
                />
              </div>

              <div className="form-actions">
                <button 
                  onClick={handleSave} 
                  className="save-btn"
                  disabled={isSubmitting || (editUsername !== username && usernameAvailable === false)}
                >
                  {isSubmitting ? 'Saving...' : 'Save Changes'}
                </button>
                <button 
                  onClick={handleCancel} 
                  className="cancel-btn"
                  disabled={isSubmitting}
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
        )}
      </div>
    </div>
  );
}

export default Profile;
