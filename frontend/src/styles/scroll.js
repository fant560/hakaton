import { theme } from './theme'

export const scrollStyle = {
  '&': {
    '::-webkit-scrollbar': {
      position: 'absolute',
      width: '6px',
      height: '100%'
    },

    '::-webkit-scrollbar-track': {
      background: theme.grey1Color
    },

    '::-webkit-scrollbar-thumb': {
      position: 'absolute',
      width: '6px',
      height: 'auto',

      border: 'none',

      background: theme.grey2Color,
      borderRadius: '12px'
    },

    '::-webkit-scrollbar-thumb:hover': {
      background: theme.grey3Color
    },

    '::-webkit-scrollbar-button': {
      height: '0px',
      width: '0px'
    },
    scrollbarColor: `${theme.grey2Color} ${theme.grey1Color}`,
    scrollbarWidth: 'thin'
  }
}
