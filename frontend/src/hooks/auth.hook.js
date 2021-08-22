import { useState, useCallback, useEffect } from 'react'

const storageName = 'userData'

export const useAuth = () => {
  const [accessToken, setAccessToken] = useState(null)
  const [userId, setUserId] = useState(null)
  const [username, setUsername] = useState(null)

  const login = useCallback((_accessToken, id, _username) => {
    setAccessToken(_accessToken)
    setUserId(id)
    setUsername(_username)

    localStorage.setItem(
      storageName,
      JSON.stringify({
        userId: id,
        accessToken: _accessToken,
        username: _username
      })
    )
  }, [])

  const logout = useCallback(() => {
    setAccessToken(null)
    setUserId(null)
    setUsername(null)
    localStorage.removeItem(storageName)
  }, [])

  useEffect(() => {
    const data = JSON.parse(localStorage.getItem(storageName))

    if (data && data.accessToken) {
      login(data.accessToken, data.userId, data.username)
    }
  }, [login])

  return { login, logout, accessToken, userId, username }
}
