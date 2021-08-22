import { useEffect, useRef } from 'react'
import { useMessage } from '../../hooks/message.hook'
import { useHttp } from '../../hooks/http.hook'
import { Form as AntForm, DatePicker, Input, Button, Upload } from 'antd'
import { UploadOutlined } from '@ant-design/icons'
import moment from 'moment'
import { formButtonStyle } from '../../pages/Login/Login.styles'
import { useAuth } from '../../hooks/auth.hook'

const UploadFileForm = ({ setIsModalVisible }) => {
  const message = useMessage()
  const formRef = useRef()
  const auth = useAuth()
  const { loading, request, error, clearError } = useHttp()

  useEffect(() => {
    message(error, true)
    clearError()
  }, [error, message, clearError])

  const handleSubmit = async values => {
    const FD = new FormData()

    FD.append('files[]', values.upload[0].originFileObj)
    FD.append('filename', values.filename)
    FD.append('dateOfRecording', values.dateOfRecording)

    const data = await request(
      '/ml/record/upload',
      'POST',
      FD,
      {
        Authorization: `Bearer ${auth.accessToken}`
      },
      true
    )
    formRef.current.resetFields()
    setIsModalVisible(false)
    message(data.response, false)
  }

  const normFile = e => {
    if (Array.isArray(e)) {
      return e
    }
    return e && e.fileList
  }

  const props = {
    beforeUpload: file => {
      const isJpgOrPng =
        file.type === 'audio/mpeg' ||
        file.type === 'video/mp4' ||
        file.type === 'audio/wav' ||
        file.type === 'audio/ogg'

      if (!isJpgOrPng) {
        message('Поддерживаемые форматы: mp3, mp4, wav, ogg', true)
        return Upload.LIST_IGNORE
      }

      return true
    },
    customRequest: ({ file, onSuccess }) => {
      setTimeout(() => {
        onSuccess('ok')
      }, 0)
    },
    maxCount: 1
  }

  return (
    <AntForm
      name="validate_other"
      onFinish={handleSubmit}
      labelCol={{ span: 7 }}
      ref={formRef}
    >
      <AntForm.Item
        label="Название файла"
        name="filename"
        rules={[
          {
            required: true,
            message: 'Введите название файла'
          }
        ]}
      >
        <Input />
      </AntForm.Item>

      <AntForm.Item
        label="Дата создания"
        name="dateOfRecording"
        rules={[
          {
            required: true,
            message: 'Введите дату создания файла'
          }
        ]}
      >
        <DatePicker
          disabledDate={current => current && current > moment().endOf('day')}
        />
      </AntForm.Item>

      <AntForm.Item
        name="upload"
        label="Загрузить файл"
        valuePropName="fileList"
        getValueFromEvent={normFile}
        rules={[
          {
            required: true,
            message: 'Загрузите файл'
          }
        ]}
      >
        <Upload {...props}>
          <Button icon={<UploadOutlined />}>Нажмите чтобы загрузить</Button>
        </Upload>
      </AntForm.Item>

      <AntForm.Item css={formButtonStyle}>
        <Button
          htmlType="submit"
          type="primary"
          disabled={loading}
          style={{ marginTop: 16 }}
        >
          Отправить
        </Button>
      </AntForm.Item>
    </AntForm>
  )
}

export default UploadFileForm
