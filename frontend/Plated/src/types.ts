export interface User {
  id: string;
  email: string;
  username: string;
  display_name: string;
  profile_pic: string;
}

export interface UserProfile {
  id: string;
  email: string;
  username: string;
  display_name: string;
  profile_pic: string;
}

export interface JWTPayload {
  email: string;
  exp: number;
  display_name?: string;
  profile_pic?: string;
}

export interface RegisterData {
  username: string;
  display_name: string;
  profile_pic?: string;
}

export interface UpdateUserData {
  username?: string;
  display_name?: string;
  profile_pic?: string;
}

export interface CheckUsernameResponse {
  exists: boolean;
}

export interface ApiError {
  error: string;
}
