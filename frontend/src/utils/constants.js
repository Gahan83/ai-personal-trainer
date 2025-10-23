export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    LOGOUT: '/auth/logout',
  },
  USERS: {
    PROFILE: '/users/profile',
  },
  WORKOUTS: {
    LIST: '/workouts',
    CREATE: '/workouts',
    DETAIL: (id) => `/workouts/${id}`,
  },
  EXERCISES: {
    LIST: '/exercises',
    CATEGORIES: '/exercises/categories',
  },
};

export const WORKOUT_TYPES = {
  STRENGTH: 'strength',
  CARDIO: 'cardio',
  FLEXIBILITY: 'flexibility',
  HIIT: 'hiit',
};

export const DIFFICULTY_LEVELS = {
  BEGINNER: 'beginner',
  INTERMEDIATE: 'intermediate',
  ADVANCED: 'advanced',
};

export const EXERCISE_CATEGORIES = {
  CHEST: 'chest',
  BACK: 'back',
  SHOULDERS: 'shoulders',
  ARMS: 'arms',
  LEGS: 'legs',
  CORE: 'core',
  CARDIO: 'cardio',
};
