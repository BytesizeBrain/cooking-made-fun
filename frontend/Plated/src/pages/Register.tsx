import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { setToken, getUserFromToken } from '../utils/auth';
import { registerUser, checkUsername } from '../utils/api';

function Register() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  
  const [username, setUsername] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [profilePic, setProfilePic] = useState('');
  const [usernameAvailable, setUsernameAvailable] = useState<boolean | null>(null);
  const [usernameCheckLoading, setUsernameCheckLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Get token from URL parameter
    const token = searchParams.get('token');
    
    if (!token) {
      // If no token, redirect to login
      navigate('/login');
      return;
    }

    // Store token
    setToken(token);

    // Get user info from token and pre-fill form
    const userInfo = getUserFromToken();
    if (userInfo) {
      setDisplayName(userInfo.display_name || '');
      setProfilePic(userInfo.profile_pic || '');
    }
  }, [searchParams, navigate]);

  // Check username availability with debounce
  useEffect(() => {
    if (!username || username.length < 3) {
      setUsernameAvailable(null);
      return;
    }

    const timeoutId = setTimeout(async () => {
      setUsernameCheckLoading(true);
      try {
        const available = await checkUsername(username);
        setUsernameAvailable(available);
      } catch (err) {
        console.error('Failed to check username:', err);
      } finally {
        setUsernameCheckLoading(false);
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [username]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!username || username.length < 3) {
      setError('Username must be at least 3 characters long');
      return;
    }

    if (!displayName || displayName.length < 1) {
      setError('Display name is required');
      return;
    }

    if (usernameAvailable === false) {
      setError('Username is already taken');
      return;
    }

    setIsSubmitting(true);

    try {
      await registerUser({
        username,
        display_name: displayName,
        profile_pic: profilePic || undefined,
      });
      
      // Registration successful, redirect to profile
      navigate('/profile');
    } catch (err: any) {
      console.error('Registration failed:', err);
      setError(err.response?.data?.error || 'Failed to complete registration. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <div className="register-header">
          <h1>Complete Your Profile</h1>
          <p>Just a few more details to get started with Plated</p>
        </div>

        <form onSubmit={handleSubmit} className="register-form">
          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label htmlFor="displayName">Display Name *</label>
            <input
              id="displayName"
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              placeholder="Your full name"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="username">Username *</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, ''))}
              placeholder="Choose a unique username"
              required
              minLength={3}
            />
            {username && username.length >= 3 && (
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
            <label htmlFor="profilePic">Profile Picture URL (Optional)</label>
            <input
              id="profilePic"
              type="url"
              value={profilePic}
              onChange={(e) => setProfilePic(e.target.value)}
              placeholder="https://example.com/your-photo.jpg"
            />
            {profilePic && (
              <div className="profile-pic-preview">
                <img src={profilePic} alt="Profile preview" onError={(e) => {
                  e.currentTarget.style.display = 'none';
                }} />
              </div>
            )}
          </div>

          <button 
            type="submit" 
            className="submit-btn"
            disabled={isSubmitting || usernameAvailable === false || !username || !displayName}
          >
            {isSubmitting ? 'Creating Profile...' : 'Complete Registration'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Register;
