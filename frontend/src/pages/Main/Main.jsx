import React, { useEffect, useState, useContext, useMemo } from 'react'
import { Button, Layout, Input, Form, Tooltip, DatePicker } from 'antd'
import moment from 'moment'
import { SearchOutlined } from '@ant-design/icons'
import { useMessage } from '../../hooks/message.hook'
import Modal from '../../components/Modal/Modal'
import UploadFileForm from '../../components/UploadFileForm/UploadFileForm'
import {
  mainPageSiderStyle,
  mainPageStyle,
  buttonStyle,
  contentStyle,
  searchStyle
} from './Main.styles'
import DocumentsList from '../../components/DocumentsList/DocumentsList'
import { useHttp } from '../../hooks/http.hook'
import { SocketContext } from '../../contexts/SocketContext'
import { AuthContext } from '../../contexts/AuthContext'

const Main = () => {
  const [isModalVisible, setIsModalVisible] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [documents, setDocuments] = useState([])

  const [startDate, setStartDate] = useState(null)
  const [endDate, setEndDate] = useState(moment().endOf('day'))

  const auth = useContext(AuthContext)
  const socket = useContext(SocketContext).socket
  const message = useMessage()
  const { loading, request } = useHttp()

  useEffect(() => {
    socket.current.onmessage = data => {
      const document = JSON.parse(data.data)
      setDocuments(prev => [document, ...prev])
      message('Добавлен новый документ', false)
    }
    // eslint-disable-next-line
  }, [])

  useEffect(() => {
    const getDocuments = async () => {
      const data = await request('/ml', 'GET', null, {
        Authorization: `Bearer ${auth.accessToken}`
      })
      setDocuments(data.documents)
    }

    getDocuments()
  }, [request, auth.accessToken])

  const handleShowModal = () => {
    setIsModalVisible(true)
  }

  const handleCloseModal = () => {
    setIsModalVisible(false)
  }

  const filteredDocuments = useMemo(() => {
    const start = moment(startDate, 'DD-MM-YYYY').valueOf()
    const end = moment(endDate, 'DD-MM-YYYY').valueOf()

    if (start && end) {
      const _documents = documents.filter(document => {
        const dateOfCreation = moment(
          document.date_of_creation,
          'DD.MM.YYYY'
        ).valueOf()

        return dateOfCreation > start && dateOfCreation < end
      })

      return _documents.sort(document => {
        return document.id
      })
    }

    return documents
  }, [documents, startDate, endDate])

  const filteredAndSearchedDocuments = useMemo(() => {
    return filteredDocuments.filter(document =>
      document.title.toLowerCase().includes(searchQuery.toLowerCase())
    )
  }, [searchQuery, filteredDocuments])

  return (
    <>
      <Layout css={mainPageStyle}>
        <Layout.Sider width="280px" css={mainPageSiderStyle}>
          <Button css={buttonStyle} onClick={handleShowModal}>
            Загрузить аудиозапись
          </Button>
          <Form css={searchStyle}>
            <Form.Item>
              <Tooltip placement="bottom" title="Найти документ">
                <Input
                  value={searchQuery}
                  onChange={e => {
                    localStorage.setItem('searchQuery', e.target.value)
                    setSearchQuery(e.target.value)
                  }}
                  prefix={<SearchOutlined />}
                  allowClear
                />
              </Tooltip>
            </Form.Item>
            <Form.Item>
              <Tooltip placement="right" title="Фильтр по дате">
                <DatePicker.RangePicker
                  disabledDate={current =>
                    current && current > moment().endOf('day')
                  }
                  defaultValue={[null]}
                  value={[startDate, endDate]}
                  onChange={dates => {
                    setStartDate(dates[0])
                    setEndDate(dates[1])
                  }}
                  bordered={true}
                  allowClear={false}
                />
              </Tooltip>
            </Form.Item>
          </Form>
        </Layout.Sider>
        <Layout.Content css={contentStyle}>
          <DocumentsList
            loading={loading}
            data={filteredAndSearchedDocuments}
          />
        </Layout.Content>
      </Layout>
      <Modal
        isModalVisible={isModalVisible}
        onClose={handleCloseModal}
        title="Загрузите документ"
      >
        <UploadFileForm setIsModalVisible={setIsModalVisible} />
      </Modal>
    </>
  )
}

export default Main
