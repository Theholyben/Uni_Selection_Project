// API Service - آماده برای اتصال به بک‌اند
// در حال حاضر از mock استفاده می‌کند

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

// دریافت توکن از localStorage
function getAccessToken() {
  return localStorage.getItem('access_token')
}

function getRefreshToken() {
  return localStorage.getItem('refresh_token')
}

// ذخیره توکن‌ها
function setTokens(access, refresh) {
  localStorage.setItem('access_token', access)
  localStorage.setItem('refresh_token', refresh)
}

// پاک کردن توکن‌ها
function clearTokens() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

// ساخت هدرهای درخواست
function getHeaders(includeAuth = true) {
  const headers = {
    'Content-Type': 'application/json',
  }
  
  if (includeAuth) {
    const token = getAccessToken()
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
  }
  
  return headers
}

// رفرش توکن
async function refreshAccessToken() {
  const refresh = getRefreshToken()
  if (!refresh) {
    throw new Error('No refresh token available')
  }

  try {
    const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh }),
    })

    if (!response.ok) {
      throw new Error('Failed to refresh token')
    }

    const data = await response.json()
    setTokens(data.access, refresh)
    return data.access
  } catch (error) {
    clearTokens()
    throw error
  }
}

// درخواست HTTP با مدیریت خودکار رفرش توکن
async function apiRequest(url, options = {}) {
  const { includeAuth = true, ...fetchOptions } = options
  
  const config = {
    ...fetchOptions,
    headers: {
      ...getHeaders(includeAuth),
      ...fetchOptions.headers,
    },
  }

  try {
    // در حالت mock، از courseService استفاده می‌کنیم
    // در حالت واقعی، اینجا باید fetch واقعی انجام شود
    const response = await fetch(`${API_BASE_URL}${url}`, config)
    
    if (response.status === 401 && includeAuth) {
      // توکن منقضی شده، سعی می‌کنیم رفرش کنیم
      try {
        await refreshAccessToken()
        // دوباره درخواست می‌زنیم
        config.headers = getHeaders(includeAuth)
        const retryResponse = await fetch(`${API_BASE_URL}${url}`, config)
        if (retryResponse.status === 401) {
          clearTokens()
          window.location.href = '/login'
          throw new Error('Unauthorized')
        }
        return retryResponse
      } catch (refreshError) {
        clearTokens()
        window.location.href = '/login'
        throw refreshError
      }
    }
    
    return response
  } catch (error) {
    console.error('API Request Error:', error)
    throw error
  }
}

// لاگین
export async function login(username, password) {
  const formData = new URLSearchParams()
  formData.append('username', username)
  formData.append('password', password)
  
  const response = await fetch(`${API_BASE_URL}/token/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
  })
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || 'نام کاربری یا رمز عبور اشتباه است')
  }
  
  const data = await response.json()
  setTokens(data.access, data.refresh)
  return data
}

// لاگ‌اوت
export function logout() {
  clearTokens()
}

// بررسی وضعیت احراز هویت
export function isAuthenticated() {
  return !!getAccessToken()
}

// Export برای استفاده در سایر بخش‌ها
export { getAccessToken, getRefreshToken, setTokens, clearTokens, apiRequest }

