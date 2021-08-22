import { useContext, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import { useMessage } from '../../hooks/message.hook'
import { useHttp } from '../../hooks/http.hook'
import { AuthContext } from '../../contexts/AuthContext'
import { Form, Input, Button } from 'antd'
import { formCardStyle, formStyle, formButtonStyle } from './Login.styles'
import { setCookie } from '../../utils'

const Login = () => {
  const auth = useContext(AuthContext)
  const message = useMessage()
  const { loading, request, error, clearError } = useHttp()
  const formRef = useRef()

  useEffect(() => {
    message(error, true)
    clearError()
  }, [error, message, clearError])

  const handleSubmit = async values => {
    try {
      const data = await request('/ml/login', 'POST', {
        username: values.username,
        password: values.password
      })

      setCookie('refreshToken', data.refresh, { secure: true })

      auth.login(data.access)
    } catch (e) {
      message(error, true)
      formRef.current.resetFields()
    }
  }

  return (
    <div css={formCardStyle}>
      <h1>Вход</h1>
      <Form
        ref={formRef}
        name="login"
        labelCol={{ span: 10 }}
        wrapperCol={{ span: 15 }}
        initialValues={{ remember: true }}
        onFinish={handleSubmit}
        css={formStyle}
      >
        <Form.Item
          label="Имя пользователя"
          name="username"
          rules={[{ required: true, message: 'Введите имя пользователя!' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Пароль"
          name="password"
          rules={[{ required: true, message: 'Введите пароль!' }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item css={formButtonStyle} wrapperCol={{ offset: 1 }}>
          <Button disabled={loading} type="primary" htmlType="submit">
            Войти
          </Button>
        </Form.Item>
        <Link to="/register">Регистрация</Link>
      </Form>
    </div>
  )
}

export default Login
