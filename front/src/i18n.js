import Vue from 'vue'
import VueI18n from 'vue-i18n'
import inflection from "inflection";

Vue.use(VueI18n)

function loadLocaleMessages() {
  const locales = require.context('./locales', true, /[A-Za-z0-9-_,\s]+\.json$/i)
  const messages = {}
  locales.keys().forEach(key => {
    const matched = key.match(/([A-Za-z0-9-_]+)\./i)
    if (matched && matched.length > 1) {
      const locale = matched[1]
      messages[locale] = locales(key)
    }
  })
  return messages
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
  locale: process.env.VUE_APP_I18N_LOCALE || 'en-US',
  fallbackLocale: process.env.VUE_APP_I18N_FALLBACK_LOCALE || 'en-US',
  messages: loadLocaleMessages(),
  dateTimeFormats,
  silentTranslationWarn: true,
  missing(lang, key) {
    if (!key) {
      return
    }
    return inflection.titleize(key.replace(/^\w+\./, ''))
  }
})
