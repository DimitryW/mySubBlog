// src/api/commentService.js
import axios from 'axios'
const API_BASE = import.meta.env.VITE_API_BASE_URL

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

// 取得某篇文章的留言列表
export function fetchComments(postId) {
  return axios.get(`${API_BASE}/api/blog/posts/${postId}/comments/`, {
    withCredentials: true,
  })
}

// 新增留言
export function addComment(postId, content, parentId = null) {
  const csrftoken = getCookie('csrftoken')
  return axios.post(
    `${API_BASE}/api/blog/posts/${postId}/comments/`,
    { content: content, parent: parentId },
    {
      withCredentials: true,
      headers: { 'X-CSRFToken': csrftoken }
    }
  )
}
