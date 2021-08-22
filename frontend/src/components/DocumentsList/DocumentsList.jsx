import React from 'react'
import { useHistory } from 'react-router-dom'
import { List, Divider } from 'antd'
import {
  listItemStyle,
  dividerStyle,
  itemListTitleStyle
} from './DocumentsList.style'
import { getCutedTitle } from './DocumentsList.utils'

const DocumentsList = ({ data, loading }) => {
  const history = useHistory()

  return (
    <List
      itemLayout="horizontal"
      dataSource={data}
      loading={loading}
      renderItem={(item, index) => (
        <>
          <List.Item
            onClick={() => history.push(`/documents/${item.id}`)}
            css={listItemStyle}
          >
            <div>
              <span>{item.id}</span>
              <span css={itemListTitleStyle}>
                {getCutedTitle(item.title, 40)}
              </span>
            </div>
            <div>{item.date_of_creation}</div>
          </List.Item>
          <Divider css={dividerStyle} />
        </>
      )}
    />
  )
}

export default DocumentsList
