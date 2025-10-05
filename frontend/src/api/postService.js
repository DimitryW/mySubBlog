// src/api/postService.js
import axios from 'axios';
const API_BASE = import.meta.env.VITE_API_BASE_URL


export function fetchPosts(page=1) {
    return axios.get(`${API_BASE}/api/blog/posts/?page=${page}`);
}

export function fetchPost(id) {
    return axios.get(`${API_BASE}/api/blog/posts/${id}/`, { withCredentials: true });
}