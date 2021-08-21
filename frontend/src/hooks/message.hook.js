import { useCallback } from 'react'
import { notification } from 'antd'
import { ExclamationCircleOutlined, SmileOutlined } from '@ant-design/icons'

export const useMessage = () => {
  return useCallback((text, isError) => {
    if (text) {
      notification.open({
        message: isError ? 'Ошибка' : 'Успех',
        description: text,
        icon: isError ? <ExclamationCircleOutlined /> : <SmileOutlined />
      })
    }
  }, [])
}
