# Plated Frontend

React + TypeScript frontend for the Plated cooking social media application.

## Features

- **Login Page**: Google OAuth authentication
- **Registration Page**: Complete user profile after OAuth
- **Profile Page**: View and edit user profile

## Setup

### Prerequisites

- Node.js 16+ and npm
- Backend server running on `http://localhost:5000`

### Installation

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
   - Copy `.env.example` to `.env` if not already present
   - Update `VITE_API_BASE_URL` if your backend runs on a different port

3. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## OAuth Flow

1. User clicks "Continue with Google" on the Login page
2. Frontend redirects to backend `/login` endpoint
3. Backend handles OAuth with Google
4. Backend redirects back to frontend `/register?token=JWT_TOKEN`
5. Frontend stores the JWT token in localStorage
6. User completes registration with username and display name
7. Frontend calls `/api/user/register` with the JWT token
8. User is redirected to their profile page

## API Integration

The frontend uses Axios with interceptors to:
- Automatically attach JWT tokens to authenticated requests
- Handle 401 errors by redirecting to login
- Provide a clean API interface for backend communication

### API Endpoints Used

- `GET /login` - Initiate Google OAuth
- `POST /api/user/register` - Complete user registration (requires JWT)
- `PUT /api/user/update` - Update user profile (requires JWT)
- `GET /api/user/check_username` - Check username availability

## Project Structure

```
src/
├── components/
│   └── ProtectedRoute.tsx    # Route wrapper for authenticated pages
├── pages/
│   ├── Login.tsx              # Login page with Google OAuth
│   ├── Register.tsx           # Registration/profile completion page
│   └── Profile.tsx            # User profile view/edit page
├── utils/
│   ├── api.ts                 # Axios instance and API functions
│   └── auth.ts                # JWT token management
├── types.ts                   # TypeScript interfaces
├── App.tsx                    # Main app with routing
├── App.css                    # Application styles
└── main.tsx                   # React entry point
```

## Testing the OAuth Flow

1. **Start the Backend**:
   ```bash
   cd backend
   python app.py
   ```

2. **Start the Frontend**:
   ```bash
   cd frontend/Plated
   npm run dev
   ```

3. **Test the Flow**:
   - Navigate to `http://localhost:5173`
   - Click "Continue with Google"
   - Log in with your Google account
   - You'll be redirected to the registration page
   - Complete your profile with username and display name
   - Click "Complete Registration"
   - You'll be redirected to your profile page
   - Test editing your profile

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Environment Variables

- `VITE_API_BASE_URL` - Backend API URL (default: `http://localhost:5000`)

## Notes

- JWT tokens are stored in localStorage with key `plated_auth_token`
- Tokens expire after 24 hours (configured in backend)
- Protected routes automatically redirect to login if not authenticated
- Username validation happens in real-time with debouncing

---

## React + TypeScript + Vite Template Information

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
