import React, { useEffect, useState, useRef } from 'react'
import { Button, Layout } from 'antd'
import Modal from '../../components/Modal/Modal'
import UploadFileForm from '../../components/UploadFileForm/UploadFileForm'
import {
  mainPageSiderStyle,
  mainPageStyle,
  buttonStyle,
  contentStyle
} from './Main.styles'
import DocumentsList from '../../components/DocumentsList/DocumentsList'
import { useHttp } from '../../hooks/http.hook'
// import { randomInteger } from '../../utils'
import { useMessage } from '../../hooks/message.hook'

const Main = () => {
  const [isModalVisible, setIsModalVisible] = useState(false)
  const { loading, request } = useHttp()
  const [documents, setDocuments] = useState([])
  const socket = useRef()
  const message = useMessage()

  useEffect(() => {
    // console.log(randomInteger(5000, 15000))
    socket.current = new WebSocket('ws://localhost:8000/ws/documents/')
    socket.current.onopen = () => {
      console.log('sending city')
      // setInterval(() => {
      socket.current.send(JSON.stringify({ game_city: 1 }))
      // }, randomInteger(5000, 15000))
    }
    socket.current.onmessage = data => {
      const document = JSON.parse(data.data)
      setDocuments(prev => [document, ...prev])
      message('Добавлен новый документ', false)
    }

    return function () {
      console.log('соединение закрыто')
      socket.current.close()
    }
  }, [])

  useEffect(() => {
    const getDocuments = async () => {
      const data = await request('/ml', 'GET', null)
      setDocuments(data.documents)
    }

    getDocuments()
  }, [request])

  const handleShowModal = () => {
    setIsModalVisible(true)
  }

  const handleCloseModal = () => {
    setIsModalVisible(false)
  }

  return (
    <>
      <Layout css={mainPageStyle}>
        <Layout.Sider width="280px" css={mainPageSiderStyle}>
          <Button css={buttonStyle} onClick={handleShowModal}>
            Загрузить аудиозапись
          </Button>
        </Layout.Sider>
        <Layout.Content css={contentStyle}>
          <DocumentsList loading={loading} data={documents} />
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
