import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const analyzeUrl = async (url) => {
    try {
        const response = await api.post('/analyze-url', { url });
        return response.data;
    } catch (error) {
        console.error('Error analyzing URL:', error);
        throw error;
    }
};

export const analyzeEmail = async (subject, body) => {
    try {
        const response = await api.post('/analyze-email', { subject, body });
        return response.data;
    } catch (error) {
        console.error('Error analyzing Email:', error);
        throw error;
    }
};

export const getHistory = async () => {
    try {
        const response = await api.get('/history');
        return response.data;
    } catch (error) {
        console.error('Error fetching history:', error);
        throw error;
    }
};

export const clearHistory = async () => {
    try {
        const response = await api.delete('/history');
        return response.data;
    } catch (error) {
        console.error('Error clearing history:', error);
        throw error;
    }
};

export default api;
