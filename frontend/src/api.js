const API_BASE = '' // 使用相对路径，vite dev server proxy 会转发 /api

function getToken() {
  return localStorage.getItem('token')
}

async function request(url, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }
  const token = getToken()
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const res = await fetch(API_BASE + url, {
    ...options,
    headers
  })

  const data = await res.json().catch(() => null)
  if (!res.ok) {
    throw { response: { data, status: res.status } }
  }
  return { data }
}

export default {
  async login(account, password) {
    return request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ account, password })
    })
  },

  async register(account, password) {
    return request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ account, password })
    })
  },

  async me() {
    return request('/api/auth/me')
  },

  async generate(topic) {
    return request('/api/paper/generate', {
      method: 'POST',
      body: JSON.stringify({ topic })
    })
  }
}
