<template>
    <div v-if="data.html" v-html="data.html"></div>
</template>

<script>
export default {
  data() {
    return {
      data: {},
      html: ""
    };
  },
  methods: {
    fetch() {
      this.$http.get("/home").then(({ data }) => {
        this.data = data;
      });
    }
  },
  created() {
    this.fetch();
  }
};
</script>
