// API Base URL with robust fallback for Gitpod environment
export const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  (window.location.hostname.includes('gitpod.io')
    ? window.location.origin.replace('4000', '8300')
    : 'http://localhost:8300');
