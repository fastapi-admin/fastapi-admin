<template>
  <div class>
    <div class="row">
      <div class="col-sm-6 col-md-3" v-for="(item, index) in data.statics" :key="index">
        <b-card class="text-white" :class="[`bg-${item.bg}`]">
          <div class="h1 text-right mb-4">
            <i :class="[item.icon]"></i>
          </div>
          <div class="h4 mb-0">{{item.value}}</div>
          <small class="text-uppercase font-weight-bold">{{item.title}}</small>
          <b-progress class="progress-white progress-xs mt-3" :value="item.progress"/>
        </b-card>
      </div>
      <!--/.col-->
    </div>
    <!--/.row-->
    <div class="jumbotron mt-3">
      <h1 class="display-4" v-html="data.title"></h1>
      <div class="lead" v-html="data.description"></div>
      <b-button v-bind="data.button" v-if="data.button">
        <i :class="[data.button.icon]" v-if="data.button.icon"></i>
        {{data.button.text}}
      </b-button>
    </div>

    <div v-if="data.html" v-html="data.html"></div>
  </div>
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
      this.$http.get("home").then(({ data }) => {
        this.data = data;
      });
    }
  },
  created() {
    this.fetch();
  }
};
</script>
