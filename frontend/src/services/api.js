import axios from "axios";

// Base URL for your FastAPI backend (adjust port as needed)
const API_URL = "http://127.0.0.1:8000/auth";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
