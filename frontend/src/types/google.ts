export type GoogleTokenResponse = {
  access_token?: string;
  error?: string;
};

export interface GoogleTokenClient {
  requestAccessToken: () => void;
}

export interface GoogleOAuth2InitConfig {
  client_id: string;
  scope: string;
  prompt?: string;
  callback: (response: GoogleTokenResponse) => void;
}

export interface GoogleOAuth2Api {
  initTokenClient: (config: GoogleOAuth2InitConfig) => GoogleTokenClient;
}

export interface GoogleAccountsApi {
  oauth2?: GoogleOAuth2Api;
}

export interface GoogleGlobalApi {
  accounts?: GoogleAccountsApi;
}

declare global {
  interface Window {
    google?: GoogleGlobalApi;
  }
}

export interface GoogleAuthConfig {
  clientId: string;
  scope?: string;
  prompt?: 'none' | 'consent' | 'select_account' | string;
}

export {};
