# Frontend-Backend Integration Notes

## Important Setup Required

### 1. ~~CORS Configuration~~ ✅ CONFIGURED

CORS is now enabled in the backend to allow frontend requests from `http://localhost:5173`.

Configuration in `backend/app.py`:
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {"origins": "http://localhost:5173"},
    r"/login": {"origins": "http://localhost:5173"},
    r"/authorize/*": {"origins": "http://localhost:5173"}
}, supports_credentials=True)
```

The configuration allows:
- All `/api/*` endpoints
- `/login` endpoint for OAuth initiation
- `/authorize/*` endpoints for OAuth callbacks
- Credentials support for cookie/session handling

### 2. ~~Backend Response Format Issue~~ ✅ RESOLVED

~~**Issue**: The `/api/user/register` endpoint currently returns a redirect:~~
```python
# OLD - DON'T USE
# return redirect(app.config['FRONTEND_URL'])

# NEW - CURRENT IMPLEMENTATION
return jsonify({"message": "User registered successfully", "user_id": new_id}), 201
```

The endpoint now correctly returns JSON responses that the frontend expects.

### 3. Environment Variables

**Backend** (`.env` file):
```
FRONTEND_URL=http://localhost:5173
SECRET_KEY=your-secret-key
CLIENT_ID=your-google-client-id
CLIENT_SECRET=your-google-client-secret
```

**Frontend** (`frontend/Plated/.env` file):
```
VITE_API_BASE_URL=http://localhost:5000
```

## OAuth Flow Implementation Details

### Step-by-Step Flow

1. **User clicks "Continue with Google"**
   - Frontend: `Login.tsx` redirects to `http://localhost:5000/login`
   - No credentials or tokens needed yet

2. **Backend initiates OAuth**
   - Backend: `/login` route redirects to Google's OAuth
   - Google authenticates the user

3. **Google redirects back to backend**
   - Backend: `/authorize/google` receives OAuth token
   - Backend creates JWT with user email and info
   - Backend redirects to `http://localhost:5173/register?token=JWT_TOKEN`

4. **Frontend receives token**
   - Frontend: `Register.tsx` extracts token from URL param
   - Frontend stores token in localStorage
   - Frontend decodes token to pre-fill display name and profile pic

5. **User completes registration**
   - Frontend: User enters username and display name
   - Frontend validates username availability in real-time
   - Frontend makes POST to `/api/user/register` with JWT in Authorization header

6. **Backend creates user**
   - Backend: Validates JWT and creates user in database
   - Backend should return JSON success response (see Issue #2 above)

7. **Frontend redirects to profile**
   - Frontend: Navigates to `/profile`
   - Profile page uses JWT to display and edit user info

## API Endpoint Summary

| Endpoint | Method | Auth Required | Purpose |
|----------|--------|---------------|---------|
| `/login` | GET | No | Start Google OAuth flow |
| `/authorize/google` | GET | No | OAuth callback (handled by backend) |
| `/api/user/register` | POST | Yes (JWT) | Complete user registration |
| `/api/user/update` | PUT | Yes (JWT) | Update user profile |
| `/api/user/check_username` | GET | No | Check if username is available |

## Testing Checklist

- [x] CORS is enabled on backend ✅
- [ ] Backend is running on port 5000
- [ ] Frontend is running on port 5173
- [ ] Environment variables are set
- [ ] Google OAuth credentials are configured
- [x] `/api/user/register` returns JSON (not redirect) ✅
- [ ] Can click "Continue with Google" and see Google login
- [ ] After Google auth, redirected to registration page with token
- [ ] Can complete registration with username
- [ ] Username availability check works
- [ ] After registration, redirected to profile page
- [ ] Can view profile information
- [ ] Can edit profile (username, display name, profile pic)
- [ ] Logout works and redirects to login

## Common Issues

### Issue: "Authorization header is missing"
**Cause**: JWT token not being sent with request
**Fix**: Check that token is stored in localStorage and axios interceptor is working

### Issue: CORS error in browser console
**Cause**: CORS not enabled on backend
**Fix**: Install flask-cors and configure as shown above

### Issue: "Failed to fetch" or network error
**Cause**: Backend not running or wrong URL
**Fix**: Ensure backend is running on port 5000 and VITE_API_BASE_URL is correct

### Issue: Redirect loop between login and profile
**Cause**: Token validation failing or expired
**Fix**: Check token expiration in JWT payload, may need to clear localStorage

### Issue: Registration succeeds but stays on registration page
~~**Cause**: Backend returns redirect instead of JSON~~
**Fix**: ✅ This has been resolved - backend now returns proper JSON response
