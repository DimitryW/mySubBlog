// src/api/topics.js
import axios from 'axios';
const API_BASE = import.meta.env.VITE_API_BASE_URL

export const getTopics = async () => {
  try {
    console.log(`${API_BASE}/api/blog/topics/`);
    const response = await axios.get(`${API_BASE}/api/blog/topics/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching topics:", error);
    throw error;
  }
};
