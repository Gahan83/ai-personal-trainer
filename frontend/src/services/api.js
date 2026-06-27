import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const PASSWORD_KEY = 'app_password';

// Attach the shared-secret gate password to every request.
api.interceptors.request.use(
  (config) => {
    const pw = localStorage.getItem(PASSWORD_KEY);
    if (pw) {
      config.headers['X-App-Password'] = pw;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// On 401 the gate password is wrong/expired — clear it and reload to re-prompt.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(PASSWORD_KEY);
      if (window.location.pathname !== '/') window.location.href = '/';
      else window.location.reload();
    }
    return Promise.reject(error);
  }
);

export default api;
