import axios from 'axios';
import { getToken, removeToken } from './auth';
import type { RegisterData, UpdateUserData, CheckUsernameResponse, UserProfile } from '../types';

// Base URL for the backend API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // If we get a 401, remove the token and redirect to login
    if (error.response?.status === 401) {
      removeToken();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Register a new user after OAuth
 */
export const registerUser = async (data: RegisterData): Promise<void> => {
  await api.post('/api/user/register', data);
};

/**
 * Get current user's profile
 */
export const getUserProfile = async (): Promise<UserProfile> => {
  const response = await api.get<UserProfile>('/api/user/profile');
  return response.data;
};

/**
 * Update user profile
 */
export const updateUser = async (data: UpdateUserData): Promise<void> => {
  await api.put('/api/user/update', data);
};

/**
 * Check if a username is available
 */
export const checkUsername = async (username: string): Promise<boolean> => {
  const response = await api.get<CheckUsernameResponse>('/api/user/check_username', {
    params: { username },
  });
  return !response.data.exists; // Return true if username is available
};

export default api;
