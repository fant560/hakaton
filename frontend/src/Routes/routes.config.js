import Main from '../pages/Main/Main'
import Login from '../pages/Login/Login'
import Register from '../pages/Register/Register'
import Document from '../pages/Document/Document'
import {
  LOGIN_PAGE,
  DOCUMENTS_PAGE,
  REGISTER_PAGE,
  DOCUMENT_PAGE
} from './routes.paths'

export const routesForAuthUsers = [
  {
    path: DOCUMENTS_PAGE,
    component: <Main />,
    exact: true
  },
  {
    path: DOCUMENT_PAGE,
    component: <Document />,
    exact: false
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
