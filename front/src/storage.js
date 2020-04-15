export default {
  get(key, defaultValue) {
    try {
      return JSON.parse(localStorage.getItem(`fastapi_admin_${key}`))
    } catch (e) {
      return defaultValue
    }
  },
  set(key, value) {
    localStorage.setItem(`fastapi_admin_${key}`, JSON.stringify(value))
  },
}
