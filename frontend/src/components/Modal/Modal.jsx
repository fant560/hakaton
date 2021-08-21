import { Modal as AntModal } from 'antd'

const Modal = ({ isModalVisible, onClose, children, title }) => {
  return (
    <AntModal
      title={title}
      visible={isModalVisible}
      footer={null}
      onCancel={onClose}
    >
      {children}
    </AntModal>
  )
}

export default Modal
