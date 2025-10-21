// src/api/topics.js
import axios from 'axios';
const API_BASE = import.meta.env.VITE_API_BASE_URL

export const getCategories = async () => {
  try {
    const response = await axios.get(`${API_BASE}/api/blog/categories/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching categories:", error);
    throw error;
  }
};

export const getCategoriesPosts = async (slug, page = 1) => {
  try {
    const res = await axios.get(`${API_BASE}/api/blog/categories/${slug}/posts/?page=${page}`)
    console.log(res.data)
    return res.data
  } catch (err) {
    console.error(err)
    throw err
  }
}
