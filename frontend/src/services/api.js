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

export default api;
