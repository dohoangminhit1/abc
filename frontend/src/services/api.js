import axios from "axios";

export const API_URL = import.meta.env.MODE === 'development' 
    ? import.meta.env.VITE_API_URL_LOCAL 
    : import.meta.env.VITE_API_URL_PROD;

const axios_instance = axios.create({
    baseURL: API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

axios_instance.interceptors.request.use(
    config => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => Promise.reject(error)
);

export default axios_instance;
