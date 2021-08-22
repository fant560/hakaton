import { scrollStyle } from '../../styles/scroll'
import { theme } from '../../styles/theme'

export const mainPageStyle = {
  height: '100%'
}

export const mainPageSiderStyle = {
  background: theme.backgroundColor2,
  padding: '20px 0px',

  '.ant-layout-sider-children': {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center'
  }
}

export const searchStyle = {
  width: '80%',
  marginTop: '24px'
}

export const buttonStyle = {
  height: '50px',
  width: '80%'
}

export const contentStyle = {
  overflow: 'auto',
  ...scrollStyle
}
