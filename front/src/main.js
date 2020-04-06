// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import _ from 'lodash'

import Vue from 'vue'
import App from './App'
import router from './router'
import store, { types } from './store'
import './http'
import i18n from './i18n'
import config from './config'
import inflection from 'inflection'
Vue.prototype.$config = config
Vue.prototype.$inflection = inflection

import { sync } from 'vuex-router-sync'

import BootstrapVue from 'bootstrap-vue'
import Snotify from 'vue-snotify'

import 'font-awesome/css/font-awesome.min.css'
import 'simple-line-icons/css/simple-line-icons.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './scss/style.scss'

import "vue-snotify/styles/material.css"
Vue.use(Snotify)

Vue.config.productionTip = false
Vue.use(BootstrapVue)

import './form'

import storage from './storage'
Vue.prototype.$storage = storage

import VueElementLoading from 'vue-element-loading'
Vue.component('BLoading', VueElementLoading)

Vue.prototype._ = _
sync(store, router)

store.dispatch(types.GET_AUTH)
store.dispatch(types.FETCH_LOCALE)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  i18n,
  watch: {
    
  },
  methods: {
    
  },
  render: h => h(App),
  
  created() {
    
    // form.init()
  }
})
