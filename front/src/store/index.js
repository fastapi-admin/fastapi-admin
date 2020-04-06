'use strict'

import Vue from 'vue'
import Vuex from 'vuex'
// import env from '../env'

import modules from './modules'
import types from './types'
export { default as types } from './types'
Vue.use(Vuex)

export default new Vuex.Store({
  modules: modules,
  state: {
    loading: false,
    downloadUrl: null
  },
  getters: {

  },
  mutations: {
    [types.DOWNLOAD](state, url) {
      state.downloadUrl = ''
      Vue.nextTick(() => {
        this.downloadUrl = url
      })
    },
    [types.START_LOADING](state) {
      state.loading = true
    },
    [types.STOP_LOADING](state) {
      state.loading = false
    },

  },
  actions: {

  }
})
