import axios from 'axios';

// Create a configured axios instance
const apiClient = axios.create();

// Force HTTPS for Gitpod environment to prevent mixed content errors
if (typeof window !== 'undefined' && window.location.hostname.includes('gitpod.io')) {
  console.log('Setting up axios interceptor for Gitpod environment');

  // Intercept requests to force HTTPS
  apiClient.interceptors.request.use((config) => {
    console.log('Axios interceptor triggered for URL:', config.url);
    if (config.url && config.url.startsWith('http://') && config.url.includes('gitpod.io')) {
      console.log('Forcing HTTPS for Gitpod request:', config.url);
      config.url = config.url.replace('http://', 'https://');
      console.log('URL converted to:', config.url);
    }
    return config;
  });

  // Intercept responses to handle redirects
  apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response && error.response.status === 307) {
        const redirectUrl = error.response.headers.location;
        console.log('Handling 307 redirect to:', redirectUrl);

        if (redirectUrl && redirectUrl.startsWith('http://') && redirectUrl.includes('gitpod.io')) {
          const httpsUrl = redirectUrl.replace('http://', 'https://');
          console.log('Converting redirect URL to HTTPS:', httpsUrl);

          // Make a new request to the HTTPS URL
          return apiClient.get(httpsUrl);
        }
      }
      return Promise.reject(error);
    },
  );
}

export default apiClient;
