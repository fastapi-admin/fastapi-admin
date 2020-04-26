<template>
  <div class="app-footer">
    <footer v-html="site.footer" v-if="site.footer"></footer>
    <footer v-else>
      <span class="ml-auto">
        GitHub
        <a href="https://github.com/long2ice/fastapi-admin">FASTAPI-ADMIN</a>
      </span>
    </footer>
  </div>
</template>
<script>
import { mapState } from "vuex";
export default {
  computed: {
    ...mapState(["site"])
  }
};
</script>
<style lang="scss">
.app-footer {
  bottom: 0;
  right: 0;
  margin-top: 10px;
  width: 100%;
  z-index: 9;
  letter-spacing: 1px;

  & > footer {
    // margin-left: 215px;
    padding: 0.5em;
    text-align: center;
  }
}
</style>
