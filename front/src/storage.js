export default {
  get(key, defaultValue) {
    try {
      return JSON.parse(localStorage.getItem(`rest_admin_${key}`))
    } catch (e) {
      return defaultValue
    }
  },
  set(key, value) {
    localStorage.setItem(`rest_admin_${key}`, JSON.stringify(value))
  },
}