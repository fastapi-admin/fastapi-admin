import Vue from 'vue'
import axios from 'axios'
import store, { types } from './store'
import _ from 'lodash'

const API_URI = process.env.VUE_APP_API_URL || '/admin/api/'
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
  const { data, status, statusText } = response
  switch (status) {
    case 422:

      break;
    case 401:
      // vm.$snotify.error('请先登录')
      store.dispatch(types.GO_LOGIN)
      break
    case 404:
      Vue.prototype.$snotify.error(String(statusText))
      break;
  }
  let msg = _.get(data, 'message', _.get(data, 'error.message', _.get(data, '0.message')))
  if (Array.isArray(msg)) {
    msg = msg[0].message
  }
  
  if (msg) {
    Vue.prototype.$snotify.error(String(msg))
  } else {
    // console.error(data)
  }
  return Promise.reject(response);
});

Vue.prototype.$http = axios

export default axios