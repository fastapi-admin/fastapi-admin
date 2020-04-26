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
    width: 100%;
    margin-top: 1vh;
    letter-spacing: 1px;
    text-align: center;
  }
</style>
