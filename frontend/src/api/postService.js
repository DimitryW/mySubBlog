// src/api/postService.js
import axios from 'axios';
const API_BASE = import.meta.env.VITE_API_BASE_URL


export function fetchPosts(page=1) {
    return axios.get(`${API_BASE}/api/blog/posts/?page=${page}`);
}

export function fetchPost(id) {
    return axios.get(`${API_BASE}/api/blog/posts/${id}/`, { withCredentials: true });
}

export function fetchMemberPost() {
  return axios.get(`${API_BASE}/api/blog/posts/members-only/`, {
    withCredentials: true
  });
}

export const getPostsByTag = async (tag, page = 1) => {
  try {
    const res = await axios.get(`${API_BASE}/api/blog/posts/tag/${tag}/`, {
      params: { page },
      withCredentials: true
    })
    return res.data
  } catch (err) {
    console.error(err)
    throw err
  }
}