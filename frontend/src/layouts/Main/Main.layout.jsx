import { useContext } from 'react'
import {
  mainLayoutStyles,
  containerStyles,
  mainLayoutHeaderStyles,
  mainLayoutContentStyles,
  headerLogoStyles,
  headerTitleStyles,
  usernameHeaderStyles
} from './Main.styles'
import { Layout, Button } from 'antd'
import { FileSyncOutlined, UserOutlined } from '@ant-design/icons'
import { AuthContext } from '../../contexts/AuthContext'

const MainLayout = ({ children }) => {
  const context = useContext(AuthContext)

  return (
    <Layout.Content css={mainLayoutStyles}>
      <div css={containerStyles}>
        <Layout.Header css={mainLayoutHeaderStyles}>
          <FileSyncOutlined css={headerLogoStyles} />
          <div css={headerTitleStyles}>Transcribify</div>
          <div css={usernameHeaderStyles}>
            <UserOutlined />
            <div>{context.username}</div>
          </div>
          <Button type="primary" onClick={context.logout}>
            Выйти
          </Button>
        </Layout.Header>
        <Layout.Content css={mainLayoutContentStyles}>
          {children}
        </Layout.Content>
      </div>
    </Layout.Content>
  )
}

export default MainLayout
