import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)

  useEffect(() => {
    // بررسی وجود توکن در localStorage
    const token = localStorage.getItem('access_token')
    if (token) {
      setIsAuthenticated(true)
      // در حالت واقعی، می‌توانیم اطلاعات کاربر را از توکن استخراج کنیم
      setUser({ username: 'admin', role: 'ADMIN' })
    }
  }, [])

  const login = (token, refreshToken) => {
    localStorage.setItem('access_token', token)
    localStorage.setItem('refresh_token', refreshToken)
    setIsAuthenticated(true)
    setUser({ username: 'admin', role: 'ADMIN' })
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setIsAuthenticated(false)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

