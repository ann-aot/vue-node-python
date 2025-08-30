// export const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8300/api/v1';

console.log('Hostname:', window.location.hostname);
export const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  (window.location.hostname.includes('gitpod.io')
    ? window.location.origin.replace('4000', '8300') + '/api/v1'
    : 'http://localhost:8300/api/v1');
