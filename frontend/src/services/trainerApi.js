import api from './api';

// Thin wrappers around the AI Personal Trainer backend (single-user).
export const trainerApi = {
  // Profile
  getProfile: () => api.get('/users/profile').then((r) => r.data),
  updateProfile: (body) => api.put('/users/profile', body).then((r) => r.data),

  // Agent
  getWeek: () => api.get('/agent/week').then((r) => r.data),
  getToday: () => api.get('/agent/today').then((r) => r.data),
  chat: (message, history = []) =>
    api.post('/agent/chat', { message, history }).then((r) => r.data),

  // Check-in (adaptive recovery)
  getTodayCheckin: () => api.get('/checkin/today').then((r) => r.data),
  submitCheckin: (body) => api.post('/checkin/', body).then((r) => r.data),
  checkinHistory: () => api.get('/checkin/history').then((r) => r.data),

  // Workouts
  completeSession: (id, body) =>
    api.post(`/workouts/${id}/complete`, body).then((r) => r.data),
  skipSession: (id) => api.post(`/workouts/${id}/skip`).then((r) => r.data),
  logSet: (id, body) => api.post(`/workouts/${id}/sets`, body).then((r) => r.data),
  history: () => api.get('/workouts/history').then((r) => r.data),
  progress: () => api.get('/workouts/progress').then((r) => r.data),

  // Nutrition
  getNudges: () => api.get('/nutrition/nudges').then((r) => r.data),
  logNutrition: (body) => api.post('/nutrition/', body).then((r) => r.data),

  // Wearables
  getWearable: () => api.get('/wearables/latest').then((r) => r.data),
  syncWearable: (body) => api.post('/wearables/sync', body).then((r) => r.data),
};

export default trainerApi;
