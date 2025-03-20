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

export default axios_instance;
