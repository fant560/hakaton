import { useEffect, useRef } from 'react'
import { Link, useHistory } from 'react-router-dom'
import { useMessage } from '../../hooks/message.hook'
import { useHttp } from '../../hooks/http.hook'
import { Form, Input, Button } from 'antd'
import { formCardStyle, formStyle, formButtonStyle } from './Register.styles'
import { LOGIN_PAGE } from '../../Routes/routes.paths'

const Register = () => {
  const message = useMessage()
  const { loading, request, error, clearError } = useHttp()
  const formRef = useRef()
  const history = useHistory()

  useEffect(() => {
    message(error, true)
    clearError()
  }, [error, message, clearError])

  const handleSubmit = async values => {
    try {
      request('/ml/register', 'POST', {
        username: values.username,
        email: values.email,
        password: values.password,
        first_name: values.firstName,
        last_name: values.lastName
      })
      message('Вы успешно зарегистрированы!', false)
      history.push(LOGIN_PAGE)
      formRef.current.resetFields()
    } catch (e) {
      message(error, true)
      formRef.current?.resetFields()
    }
  }

  return (
    <div css={formCardStyle}>
      <h1>Регистрация</h1>
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
          label="Имя"
          name="firstName"
          rules={[{ required: true, message: 'Введите имя!' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Фамилия"
          name="lastName"
          rules={[{ required: true, message: 'Введите фамилию!' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Почта"
          name="email"
          rules={[
            { required: true, message: 'Введите почту!' },
            {
              required: true,
              type: 'email',
              message: 'Не соответствует типу email!'
            }
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Пароль"
          name="password"
          rules={[
            { required: true, message: 'Введите пароль!' },
            () => ({
              validator(_, value) {
                if (value.length >= 8) {
                  return Promise.resolve()
                }
                return Promise.reject(new Error('Пароль не менее 8 символов!'))
              }
            })
          ]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item
          label="Подтвердите пароль"
          name="confirm"
          dependencies={['password']}
          rules={[
            {
              required: true,
              message: 'Подтвердите пароль!'
            },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue('password') === value) {
                  return Promise.resolve()
                }
                return Promise.reject(new Error('Пароли не совпадают!'))
              }
            })
          ]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item css={formButtonStyle} wrapperCol={{ offset: 1 }}>
          <Button disabled={loading} type="primary" htmlType="submit">
            Войти
          </Button>
        </Form.Item>
        <Link to="/login">Уже зарегистрированы ?</Link>
      </Form>
    </div>
  )
}

export default Register
