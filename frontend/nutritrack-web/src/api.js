import axios from 'axios';

const API = axios.create({
    baseURL: 'http://localhost:5001',
});

export const analyticsAPI = {
    getDaily: async (userId, date) => (await API.get(`/analytics/daily?user_id=${userId}&date=${date}`)).data,
    getWeekly: async (userId, date) => (await API.get(`/analytics/weekly?user_id=${userId}&date=${date}`)).data,
    getMonthly: async (userId, date) => (await API.get(`/analytics/monthly?user_id=${userId}&date=${date}`)).data,
    getTopFoods: async (userId) => (await API.get(`/analytics/top-foods?user_id=${userId}`)).data
};

export const usersAPI = {
    getAll: async () => (await API.get('/users')).data,
    create: async (data) => (await API.post('/users', data)).data,
    delete: async (id) => (await API.delete(`/users/${id}`)).data
};

export const foodsAPI = {
    getAll: async () => (await API.get('/foods')).data,
    create: async (data) => (await API.post('/foods', data)).data,
    delete: async (id) => (await API.delete(`/foods/${id}`)).data
};

export const mealsAPI = {
    create: async (data) => (await API.post('/meals', data)).data,
    addItem: async (mealId, data) => (await API.post(`/meals/${mealId}/items`, data)).data,
    getDetails: async (mealId) => (await API.get(`/meals/${mealId}`)).data,
    // Add this new line:
    getDailyMeals: async (userId, date) => (await API.get(`/meals/daily?user_id=${userId}&date=${date}`)).data
};

export const goalsAPI = {
    get: async (userId) => (await API.get(`/goals/user/${userId}`)).data,
    create: async (data) => (await API.post('/goals', data)).data,
    update: async (userId, data) => (await API.put(`/goals/user/${userId}`, data)).data
};

