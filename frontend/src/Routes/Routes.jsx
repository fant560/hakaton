import React from 'react'
import { Route, Switch, Redirect } from 'react-router-dom'
import LoginLayout from '../layouts/Login/Login.layout'
import MainLayout from '../layouts/Main/Main.layout'
import { routesForAuthUsers, routesForNotAuthUsers } from './routes.config'
import { LOGIN_PAGE, DOCUMENTS_PAGE } from './routes.paths'

const useRoutes = isAuthenticated => {
  if (isAuthenticated) {
    return (
      <MainLayout>
        <Switch>
          {routesForAuthUsers.map(route => (
            <Route key={route} exact={route.exact} path={route.path}>
              {route.component}
            </Route>
          ))}
          <Redirect to={DOCUMENTS_PAGE} />
        </Switch>
      </MainLayout>
    )
  }

  return (
    <LoginLayout>
      <Switch>
        {routesForNotAuthUsers.map(route => (
          <Route key={route} exact={route.exact} path={route.path}>
            {route.component}
          </Route>
        ))}
      </Switch>
      <Redirect to={LOGIN_PAGE} />
    </LoginLayout>
  )
}

export default useRoutes
