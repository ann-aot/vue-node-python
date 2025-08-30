// API Base URL with fallback for local development
// VITE_API_BASE_URL should contain the full API base URL (e.g., https://8300-workspace.gitpod.io/api/v1)
// The /api/v1 path is automatically appended if not present
const baseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8300';
export const API_BASE = baseUrl.endsWith('/api/v1') ? baseUrl : baseUrl + '/api/v1';

// Debug logging
console.log('Environment VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);
console.log('Computed baseUrl:', baseUrl);
console.log('baseUrl.endsWith("/api/v1"):', baseUrl.endsWith('/api/v1'));
console.log('Final API_BASE:', API_BASE);
console.log('Expected full URL for /states:', API_BASE + '/states');
