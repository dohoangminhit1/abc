import axios from "axios";

const API_URL = "http://127.0.0.1:8000/auth";

const axios_instance = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default axios_instance;
