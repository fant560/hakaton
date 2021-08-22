import { useContext, useRef, useEffect } from 'react'
import { Link } from 'react-router-dom'
import jwt from 'jsonwebtoken'
import {
  mainLayoutStyles,
  containerStyles,
  mainLayoutHeaderStyles,
  mainLayoutContentStyles,
  headerLogoStyles,
  headerTitleStyles,
  usernameHeaderStyles,
  linkLogoStyles
} from './Main.styles'
import { Layout, Button } from 'antd'
import { FileSyncOutlined, UserOutlined } from '@ant-design/icons'
import { AuthContext } from '../../contexts/AuthContext'
import { DOCUMENTS_PAGE } from '../../Routes/routes.paths'
import { SocketContext } from '../../contexts/SocketContext'
import { useHttp } from '../../hooks/http.hook'
import { getCookie } from '../../utils'

const MainLayout = ({ children }) => {
  const auth = useContext(AuthContext)
  const socket = useRef()
  const { request } = useHttp()

  useEffect(() => {
    const getAccessToken = async () => {
      const decodedToken = jwt.decode(auth.accessToken, { complete: true })
      const dateNow = new Date()

      if (decodedToken.payload.exp < dateNow.getTime()) {
        const data = await request('/ml/token-refresh', 'POST', {
          refresh: getCookie('refreshToken')
        })

        const user = await request('/ml/user', 'GET', null, {
          Authorization: `Bearer ${data.access}`
        })

        auth.login(data.access, user.id, user.username)
      }
    }

    getAccessToken()
    // eslint-disable-next-line
  }, [])

  useEffect(() => {
    socket.current = new WebSocket('ws://web:8000/ws/documents/')
    socket.current.onopen = () => {
      console.log('соединение открыто')
      socket.current.send(JSON.stringify({ game_city: 1 }))
    }

    return function () {
      console.log('соединение закрыто')
      socket.current.close()
    }
  }, [])

  return (
    <SocketContext.Provider
      value={{
        socket
      }}
    >
      <Layout.Content css={mainLayoutStyles}>
        <div css={containerStyles}>
          <Layout.Header css={mainLayoutHeaderStyles}>
            <Link to={DOCUMENTS_PAGE} css={linkLogoStyles}>
              <FileSyncOutlined css={headerLogoStyles} />
              <div css={headerTitleStyles}>Transcribify</div>
            </Link>

            <div css={usernameHeaderStyles}>
              <UserOutlined />
              <div>{auth.username}</div>
            </div>
            <Button type="primary" onClick={auth.logout}>
              Выйти
            </Button>
          </Layout.Header>
          <Layout.Content css={mainLayoutContentStyles}>
            {children}
          </Layout.Content>
        </div>
      </Layout.Content>
    </SocketContext.Provider>
  )
}

export default MainLayout
