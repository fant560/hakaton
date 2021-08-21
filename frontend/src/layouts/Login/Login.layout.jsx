import { Layout } from 'antd'
import { loginLayoutStyles } from './Login.styles'

const LoginLayout = ({ children }) => {
  return <Layout.Content style={loginLayoutStyles}>{children}</Layout.Content>
}

export default LoginLayout
