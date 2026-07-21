import axios from 'axios';

// Point this to your Flask backend
const API = axios.create({
    baseURL: 'http://localhost:5001',
});

export const analyticsAPI = {
    getDaily: async (userId, date) => {
        const response = await API.get(`/analytics/daily?user_id=${userId}&date=${date}`);
        return response.data;
    },
    getWeekly: async (userId, date) => {
        const response = await API.get(`/analytics/weekly?user_id=${userId}&date=${date}`);
        return response.data;
    },
    getTopFoods: async (userId) => {
        const response = await API.get(`/analytics/top-foods?user_id=${userId}`);
        return response.data;
    }
};

export const mealsAPI = {
    // We will add meal endpoints here later
};