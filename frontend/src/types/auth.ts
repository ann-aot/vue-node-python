export interface AuthUserProfile {
  id: string;
  email: string;
  name: string;
  avatarUrl?: string;
}

export interface AuthState {
  isAuthenticated: boolean;
  accessToken?: string;
  idToken?: string;
  user?: AuthUserProfile;
}

//
