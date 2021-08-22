import { theme } from '../../styles/theme'

export const mainLayoutStyles = {
  height: '100vh',
  background: theme.backgroundColor
}

export const mainLayoutHeaderStyles = {
  background: theme.backgroundColor2,
  display: 'flex',
  alignItems: 'center',
  borderRadius: ' 0 0 5px 5px',
  marginBottom: '20px'
}

export const headerLogoStyles = {
  fontSize: '40px',
  marginRight: '10px'
}

export const usernameHeaderStyles = {
  marginLeft: 'auto',
  fontSize: '1rem',
  marginRight: '20px',
  display: 'flex',
  alignItems: 'center',
  gap: '5px'
}

export const headerTitleStyles = {
  fontSize: '25px'
}

export const mainLayoutContentStyles = {
  background: theme.backgroundColor2,
  height: 'calc(100% - 84px)',
  borderRadius: '5px 5px 0 0',
  overflow: 'hidden'
}

export const containerStyles = {
  margin: '0 auto',
  maxWidth: '1000px',
  height: '100%',
  padding: '0 20px'
}

export const linkLogoStyles = {
  display: 'flex',
  alignItems: 'center',
  color: 'rgba(0, 0, 0, 0.85)',
  '&:hover': {
    color: 'rgba(0, 0, 0, 0.85)'
  }
}
