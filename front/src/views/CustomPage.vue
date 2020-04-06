<template>
  <div>
    <custom-component :config="page"></custom-component>
  </div>
</template>
<style>
.nopadding {
  padding: 0 !important;
}
</style>
<script>
export default {
  props: {},
  data() {
    return {
      loaded: false,
      name: null,
      page: null
    };
  },

  computed: {
    uri() {
      return this.$route.params.uri.replace(/\./g, "/");
    }
  },
  watch: {
    $route: "fetch"
  },
  methods: {
    fetch() {
      this.fetchPage();
    },
    render() {},
    fetchPage() {
      this.$http.get(this.uri).then(({ data }) => {
        data.name = "server-page-" + new Date().getTime().toString();
        this.page = Object.assign({}, data);
      });
    },

    onSuccess(data) {
      const { message, then, redirect } = data;
      if (message) {
        this.$snotify.success(message);
      }
      if (then) {
        eval(then);
      } else if (redirect) {
        this.$router.push({ path: redirect });
      } else {
        this.$router.go(-1);
      }
    }
  },
  mounted() {},
  created() {
    this.fetchPage();
  }
};
</script>

