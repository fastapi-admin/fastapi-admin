<template>
  <div class="app-footer">
    <footer v-html="site.footer" v-if="site.footer"></footer>
    <footer v-else>
      <span class="ml-auto">
        GitHub
        <a href="https://github.com/long2ice/fastapi-admin">FASTAPI-ADMIN</a> - FastAPI Admin Dashboard
      </span>
    </footer>
  </div>
</template>
<script>
  import {mapState} from "vuex";

  export default {
    computed: {
      ...mapState(["site"])
    }
  };
</script>
<style lang="scss">
  .app-footer {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    text-align: center;
  }
</style>
