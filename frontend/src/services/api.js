import axios from "axios";

const axios_instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}/auth`, // Use VITE_API_URL from .env
  headers: {
    "Content-Type": "application/json",
  },
});

export default axios_instance;
