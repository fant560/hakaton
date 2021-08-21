import { theme } from '../../styles/theme'

export const listItemStyle = {
  padding: '30px 50px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  cursor: 'pointer',
  transition: 'all .3s ease',
  '&:hover': {
    backgroundColor: theme.backgroundColor2,
    transform: 'scale(1.1)'
  },
  fontSize: '1rem'
}

export const dividerStyle = {
  margin: 0,
  backgroundColor: theme.backgroundColor3
}

export const itemListTitleStyle = {
  marginLeft: '10px',
  overflow: 'hidden',
  textOverflow: 'ellipsis',
  whiteSpace: 'pre'
}
