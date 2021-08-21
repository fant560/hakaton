import { useState, useCallback } from 'react'

const getErrorType = errors => {
  if (errors.hasOwnProperty('error')) {
    return errors.error[0]
  } else if (errors.hasOwnProperty('email')) {
    return errors.email[0]
  } else if (errors.hasOwnProperty('username')) {
    return errors.username[0]
  } else {
    return
  }
}

export const useHttp = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const request = useCallback(
    async (
      url,
      method = 'GET',
      body = null,
      headers = {},
      isFormData = false
    ) => {
      setLoading(true)
      try {
        if (body && !isFormData) {
          body = JSON.stringify(body)
          headers['Content-Type'] = 'application/json'
        }

        const response = await fetch(url, { method, body, headers })
        const data = await response.json()

        const errors = getErrorType(data.errors || {})

        if (!response.ok) {
          throw new Error(errors)
        }

        setLoading(false)

        return data
      } catch (e) {
        setLoading(false)
        setError(e.message)
        throw e
      }
    },
    []
  )

  const clearError = useCallback(() => setError(null), [])

  return { loading, request, error, clearError }
}
