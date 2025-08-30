// API Base URL with robust fallback for Gitpod environment
// VITE_API_BASE_URL should contain just the base URL (e.g., https://8300-workspace.gitpod.io)
// The /api/v1 path is automatically appended here

let baseUrl =
  import.meta.env.VITE_API_BASE_URL ||
  (window.location.hostname.includes('gitpod.io')
    ? window.location.origin.replace('4000-', '8300-').replace(':4000', ':8300')
    : window.location.protocol === 'https:'
      ? 'https://localhost:8300'
      : 'http://localhost:8300');

// Force HTTPS for Gitpod environment to prevent mixed content errors
if (window.location.hostname.includes('gitpod.io') && baseUrl.startsWith('http://')) {
  console.log('Forcing HTTPS for Gitpod environment in constants');
  baseUrl = baseUrl.replace('http://', 'https://');
}

// Additional safety check: ensure Gitpod URLs are always HTTPS
if (
  window.location.hostname.includes('gitpod.io') &&
  baseUrl.includes('gitpod.io') &&
  !baseUrl.startsWith('https://')
) {
  console.log('Additional safety: forcing HTTPS for Gitpod URL');
  baseUrl = baseUrl.replace('http://', 'https://');
}

export const API_BASE = baseUrl + '/api/v1';

// Debug logging
console.log('Environment VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);
console.log('Current hostname:', window.location.hostname);
console.log('Current origin:', window.location.origin);
console.log('Current protocol:', window.location.protocol);
console.log('Computed base URL:', baseUrl);
console.log('Final API_BASE:', API_BASE);
console.log('Is Gitpod environment:', window.location.hostname.includes('gitpod.io'));
