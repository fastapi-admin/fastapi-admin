import Vue from 'vue'
import axios from 'axios'
import store, {types} from './store'
import _ from 'lodash'

const API_URI = process.env.VUE_APP_API_URL || 'http://127.0.0.1:8000/admin/'
global.API_URI = API_URI
axios.defaults.baseURL = API_URI
global.LOADING_ENABLED = true
axios.interceptors.request.use(config => {
  global.LOADING_ENABLED && store.commit(types.START_LOADING)
  config.headers.Authorization = 'Bearer ' + store.state.auth.token
  return config
})
axios.interceptors.response.use(response => {
  store.commit(types.STOP_LOADING)
  global.LOADING_ENABLED = true
  const pageHeader = _.get(response, 'data._meta.page_header')
  store.commit(types.SET_PAGE_HEADER, pageHeader)
  return response;
}, ({response}) => {
  store.commit(types.STOP_LOADING)
  const {data, status, statusText} = response
  switch (status) {
    case 401:
      store.dispatch(types.GO_LOGIN)
      break
    case 404:
      Vue.prototype.$snotify.error(String(statusText))
      break;
    default:
      let msg = _.get(data, 'msg')
      if (msg) {
        Vue.prototype.$snotify.error(String(msg))
      }
  }
  return Promise.reject(response);
});

Vue.prototype.$http = axios

export default axios
