import Main from '../pages/Main/Main'
import Login from '../pages/Login/Login'
import Register from '../pages/Register/Register'
import { LOGIN_PAGE, MAIN_PAGE, REGISTER_PAGE } from './routes.paths'

export const routesForAuthUsers = [
  {
    path: MAIN_PAGE,
    component: <Main />,
    exact: true
  }
]

export const routesForNotAuthUsers = [
  {
    path: LOGIN_PAGE,
    component: <Login />,
    exact: false
  },
  {
    path: REGISTER_PAGE,
    component: <Register />,
    exact: false
  }
]
