import { BrowserRouter as Router } from 'react-router-dom'
import { useAuth } from './hooks/auth.hook'
import { AuthContext } from './contexts/AuthContext'
import useRoutes from './Routes/Routes'

const App = () => {
  const { accessToken, login, logout, userId, username } = useAuth()
  const isAuthenticated = !!accessToken
  const routes = useRoutes(isAuthenticated)

  return (
    <AuthContext.Provider
      value={{
        accessToken,
        login,
        logout,
        userId,
        username,
        isAuthenticated
      }}
    >
      <Router>{routes}</Router>
    </AuthContext.Provider>
  )
}

export default App
