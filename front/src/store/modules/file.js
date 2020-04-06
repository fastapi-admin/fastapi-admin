import types from '../types'
import http from '../../http'

export default {
  state: {
    locale: null,
  },
  mutations: {
    [types.SHOW_FILE_BROWSER](state, params) {

    },
  },
  actions: {
    [types.FETCH_ONLINE_FILES]({ commit }) {
      http.get('files', { params: params }).then(({ data }) => {

      })
    }
  }
}