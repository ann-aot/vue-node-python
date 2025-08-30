// API Base URL with robust fallback for Gitpod environment
// VITE_API_BASE_URL should contain just the base URL (e.g., https://8300-workspace.gitpod.io)
// The /api/v1 path is automatically appended here

const baseUrl =
  import.meta.env.VITE_API_BASE_URL ||
  (window.location.hostname.includes('gitpod.io')
    ? window.location.origin.replace('4000-', '8300-').replace(':4000', ':8300')
    : window.location.protocol === 'https:'
      ? 'https://localhost:8300'
      : 'http://localhost:8300');

export const API_BASE = baseUrl + '/api/v1';

// Debug logging
console.log('Environment VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);
console.log('Current hostname:', window.location.hostname);
console.log('Current origin:', window.location.origin);
console.log('Current protocol:', window.location.protocol);
console.log('Computed base URL:', baseUrl);
console.log('Final API_BASE:', API_BASE);
