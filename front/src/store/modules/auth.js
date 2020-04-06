import types from '../types'
import router from '../../router'
import site from './site'
import storage from '../../storage'

export default {
  state: {
    user: null,
    token: null
  },
  mutations: {
    [types.SET_AUTH](state, data) {
      if (!data) {
        data = {}
      }
      state.user = data.user
      state.token = data.token
      storage.set('auth', data)
    },
  },
  actions: {
    [types.GET_AUTH]({ commit }) {
      let auth = {}
      try {
        auth = storage.get('auth')
      } catch (e) {
        auth = {
          token: null,
          user: null
        }
      }
      commit(types.SET_AUTH, auth)
    },
    [types.GO_LOGIN](){
      // global.console.log(site.state)
      if (!site.state.login_url) {
        return router.push({name: 'login'})
      } else {
        return location.href = site.state.login_url
      }
    }
  }
}