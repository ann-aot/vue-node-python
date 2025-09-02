import { reactive } from 'vue';
import type { AuthState, AuthUserProfile } from '../types/auth';

// Basic global auth store using Vue reactive. For larger apps, switch to Pinia.
export const authState = reactive<AuthState>({
  isAuthenticated: false,
});

//

export function restoreAuthFromStorage(): void {
  const raw = localStorage.getItem('authState');
  if (!raw) return;
  try {
    const saved = JSON.parse(raw) as AuthState;
    authState.isAuthenticated = !!saved.isAuthenticated;
    authState.accessToken = saved.accessToken;
    authState.idToken = saved.idToken;
    authState.user = saved.user;
  } catch {}
}

export function persistAuthToStorage(): void {
  const toSave: AuthState = {
    isAuthenticated: authState.isAuthenticated,
    accessToken: authState.accessToken,
    idToken: authState.idToken,
    user: authState.user,
  };
  localStorage.setItem('authState', JSON.stringify(toSave));
}

declare global {
  interface Window {
    google?: any;
  }
}

export interface GoogleAuthConfig {
  clientId: string;
  scope?: string;
  prompt?: 'none' | 'consent' | 'select_account' | string;
}

export async function signInWithGoogle(config: GoogleAuthConfig): Promise<void> {
  // Use One Tap or Button with Google Identity Services OAuth 2.0 Token Client
  return new Promise((resolve, reject) => {
    try {
      const { clientId, scope, prompt } = config;
      if (!window.google?.accounts?.oauth2) {
        reject(new Error('Google Identity Services not loaded'));
        return;
      }

      const tokenClient = window.google.accounts.oauth2.initTokenClient({
        client_id: clientId,
        scope: scope ?? 'openid email profile',
        prompt: prompt ?? 'select_account',
        callback: (response: any) => {
          if (response && response.access_token) {
            // Get ID token via code flow not supported here; alternatively use "initCodeClient".
            // For basic profile: fetch userinfo endpoint.
            fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
              headers: { Authorization: `Bearer ${response.access_token}` },
            })
              .then((r) => r.json())
              .then((profile) => {
                const user: AuthUserProfile = {
                  id: profile.sub,
                  email: profile.email,
                  name: profile.name,
                  avatarUrl: profile.picture,
                };
                authState.isAuthenticated = true;
                authState.accessToken = response.access_token;
                authState.user = user;
                persistAuthToStorage();
                resolve();
              })
              .catch((err) => reject(err));
          } else if (response && response.error) {
            reject(new Error(response.error));
          } else {
            reject(new Error('Unknown Google response'));
          }
        },
      });

      tokenClient.requestAccessToken();
    } catch (err) {
      reject(err);
    }
  });
}

export function logout(): void {
  authState.isAuthenticated = false;
  authState.accessToken = undefined;
  authState.idToken = undefined;
  authState.user = undefined;
  localStorage.removeItem('authState');
}
