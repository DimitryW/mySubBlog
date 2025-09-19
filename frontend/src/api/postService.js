// src/api/postService.js
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export function fetchPosts() {
    return axios.get(`${API_BASE}/posts/`);
}

export function fetchPost(id) {
    return axios.get(`${API_BASE}/posts/${id}/`);
}