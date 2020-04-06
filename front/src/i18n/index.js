import Vue from 'vue'
import VueI18n from 'vue-i18n'
import inflection from 'inflection'

Vue.use(VueI18n)

const messages = {
  "en-US": require('./en-US.json'),
  "zh-CN": require('./zh-CN.json')
}

const dateTimeFormats = {
  'en-US': {
    short: {
      month: 'short', day: 'numeric',
    },
    long: {
      month: 'short', day: 'numeric',
      hour: 'numeric', minute: 'numeric'
    }
  },
  'zh-CN': {
    short: {
      month: 'short', day: 'numeric'
    },
    long: {
      month: 'short', day: 'numeric',
      hour: 'numeric', minute: 'numeric', hour12: false
    }
  }
}

export default new VueI18n({
  locale: 'en-US',
  messages,
  dateTimeFormats,
  silentTranslationWarn: true,
  missing(lang, key) {
    if (!key) {
      return
    }
    return inflection.titleize(key.replace(/^\w+\./, ''))
  }
})