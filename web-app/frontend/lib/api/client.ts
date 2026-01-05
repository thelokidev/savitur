import axios from 'axios';

// In production, NEXT_PUBLIC_API_URL must be set to the Render backend URL
// In development, it defaults to localhost:8000
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      const status = error.response.status;
      const detail = error.response.data?.detail || 'An error occurred';

      // User-friendly error messages
      let message = detail;
      if (status === 400) {
        message = `Invalid input: ${detail}`;
      } else if (status === 404) {
        message = 'Resource not found';
      } else if (status === 500) {
        message = `Server error: ${detail}`;
      } else if (status === 422) {
        // Validation error
        const errors = error.response.data?.detail;
        if (Array.isArray(errors)) {
          message = errors.map((e: any) => `${e.loc.join('.')}: ${e.msg}`).join(', ');
        }
      }

      throw new Error(message);
    } else if (error.request) {
      // Request made but no response
      throw new Error('Unable to connect to server. Please check if the backend is running.');
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
);

export default apiClient;


