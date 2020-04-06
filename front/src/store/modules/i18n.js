import types from '../types'
import storage from '../../storage'
import i18n from '../../i18n'

export default {
  state: {
    locale: null,
  },
  mutations: {
    [types.SET_LOCALE](state, locale) {
      state.locale = locale
      storage.set('locale', locale)
      i18n.locale = locale
    },
  },
  getters: {
    currentLanguage(state){
      return String(state.locale).replace(/-\w+/, '')
    }
  },
  actions: {
    [types.FETCH_LOCALE]({commit}){
      const cachedLocale = storage.get('locale')
      if (cachedLocale) {
        
        commit(types.SET_LOCALE, cachedLocale)
      }
    }
  }
}