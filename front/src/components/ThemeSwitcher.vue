<template>
  <div class="m-4" v-if="$store.state.site.theme_switcher">
    <b-select :options="themeOptions" v-model="theme"></b-select>
  </div>
</template>

<script>
import types from "../store/types.js";

export default {
  computed: {
    theme: {
      get() {
        return this.$store.state.site.theme;
      },
      set(val) {
        this.$store.commit(types.SET_THEME, val);
      }
    }
  },
  data() {
    return {
      themeOptions: `
      cerulean  darkly    litera    materia   sandstone slate     superhero
      cosmo     flatly    lumen     minty     simplex   solar     united
      cyborg    journal   lux       pulse     sketchy   spacelab  yeti
      `.split(/\s+/)
    };
  },
  created() {
    this.theme = this.$storage.get("theme") || 'cosmo';
  }
};
</script>

