<template>
  <div id="app">
    <router-view></router-view>
    <vue-snotify></vue-snotify>
    <div v-html="$store.state.site.html"></div>
  </div>
</template>

<script>
  import {mapState} from "vuex";
  import {types} from "./store";

  export default {
    name: "app",
    components: {},
    data() {
      return {
        frameSrc: "",
        path: []
      };
    },
    watch: {
      "site.name"(name) {
        window.document.title = name || "FASTAPI-ADMIN DASHBOARD";
      },
      "site.skin"(name) {
        const tag = document.getElementById("css-skin");
        tag.setAttribute(
          "href",
          `https://cdn.bootcss.com/bootswatch/4.1.1/${name}/bootstrap.min.css`
        );
      },
      "site.css"(files) {
        files.map(item => {
          const tag = document.createElement("link");
          tag.setAttribute("href", item);
          tag.setAttribute("rel", "stylesheet");
          document.head.appendChild(tag);
        });
      },
      "site.js"(files) {
        files.map(item => {
          const tag = document.createElement("script");
          tag.setAttribute("src", item);
          document.body.appendChild(tag);
        });
      },
      "$route.path"() {
        this.$store.dispatch(types.FETCH_PAGE_HEADER);
      }
    },
    computed: {
      ...mapState(["site"])
    },
    created() {
      this.$store.dispatch(types.FETCH_SITE);
    }
  };
</script>

<style>
  body {
    /* background: darkgrey !important; */
  }

  #app {
  }
</style>
