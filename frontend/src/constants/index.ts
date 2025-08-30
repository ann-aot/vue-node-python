// API Base URL with robust fallback for Gitpod environment
// VITE_API_BASE_URL should contain just the base URL (e.g., https://8300-workspace.gitpod.io)
// The /api/v1 path is automatically appended here
export const API_BASE =
  (import.meta.env.VITE_API_BASE_URL ||
    (window.location.hostname.includes('gitpod.io')
      ? window.location.origin.replace('4000', '8300')
      : 'http://localhost:8300')) + '/api/v1';
