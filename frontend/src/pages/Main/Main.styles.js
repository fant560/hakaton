import { scrollStyle } from '../../styles/scroll'
import { theme } from '../../styles/theme'

export const mainPageStyle = {
  height: '100%'
}

export const mainPageSiderStyle = {
  background: theme.backgroundColor2,
  display: 'flex',
  justifyContent: 'center',
  padding: '20px'
}

export const buttonStyle = {
  height: '50px'
}

export const contentStyle = {
  overflow: 'auto',
  ...scrollStyle
}
