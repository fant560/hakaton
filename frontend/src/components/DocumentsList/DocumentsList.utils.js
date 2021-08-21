export const getCutedTitle = (title, limit) => {
  if (title.length <= limit) {
    return title
  }
  return `${title.slice(0, limit)}...`
}
