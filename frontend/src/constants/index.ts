// API Base URL with fallback for local development
export const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8300/api/v1';

// Debug logging
console.log('Environment VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);
console.log('Computed API_BASE:', API_BASE);
