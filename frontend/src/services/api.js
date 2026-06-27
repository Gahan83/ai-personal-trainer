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

// On 401 the gate password is wrong/expired — clear it and let the caller
// (AccessGate) re-prompt. Do NOT reload here: the gate's own probe returns 401
// when a password is required, and reloading would cause an infinite loop.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(PASSWORD_KEY);
    }
    return Promise.reject(error);
  }
);

export default api;
