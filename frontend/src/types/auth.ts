export interface AuthUserProfile {
  id: string;
  email: string;
  name: string;
  avatarUrl?: string;
  dob?: string; // ISO date string
}

export interface AuthState {
  isAuthenticated: boolean;
  accessToken?: string;
  idToken?: string;
  user?: AuthUserProfile;
}

//
