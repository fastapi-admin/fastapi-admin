<template>
  <!-- <component :is="tag" :header="header"> -->
  <div class="data-form">
    <div class="row d-none">
      <div class="col col-md-8">
        <legend
          v-if="model[$config.primaryKey] && false"
        >{{$t('actions.edit')}}: {{model[$config.primaryKey]}}</legend>
      </div>
      <div class="col col-md-4 text-right hidden-sm-down">
        <b-btn @click="$router.go(-1)">{{$t('actions.back')}}</b-btn>
        <b-btn variant="primary" @click="$refs.form.submitForm()">{{$t('actions.save')}}</b-btn>
      </div>
    </div>
    <b-form-builder
      :languages="$store.state.site.languages"
      group-by="group"
      v-if="loaded"
      :auth="auth"
      :layout="layout"
      :fields="fields"
      ref="form"
      v-model="model"
      :action="resourceUri"
      :method="method"
      @success="onSuccess"
    ></b-form-builder>
  </div>
  <!-- </component> -->
</template>

<script>
import { mapState, mapGetters } from "vuex";
import _ from "lodash";

export default {
  components: {},
  props: {
    resource: {
      type: String,
      required: true
    },
    id: {
      default: "",
      required: true
    },
    formPath: {
      type: String,
      default: "form",
      required: false
    }
  },
  data() {
    return {
      redirect: -1,
      loaded: false,
      choices: {},
      fields: {},
      model: {},
      errors: [],
      tag: "b-card",
      header: `
        ${_.get(this.currentMenu, "name", "") || ""}
        <small> ${this.resource.toUpperCase()} </small>
      `
    };
  },
  watch: {
    id: "fetchForm",
    "site.fetched"(val){
      if (val) {
        this.fetchForm(true)
      }
    },
  },
  computed: {
    resourceUri() {
      let url = [this.site.resource_prefix, this.resource, this.id]
        .filter(v => v)
        .join("/");
      let group = this.$route.params.group;
      if (group) {
        url += "?group=" + group;
      }
      return url;
    },
    formUri() {
      let url = [this.site.resource_prefix, this.resource, this.formPath]
        .filter(v => v)
        .join("/");
      url += "?id=" + (this.id || "");
      return url;
    },
    isNew() {
      return !this.id;
    },
    method() {
      return this.isNew ? "post" : "put";
    },
    with() {
      return _.filter(
        _.map(this.fields, v => v.ref && v.ref.split(".").shift())
      );
    },
    ...mapState(["nav", "auth", "site"]),
    ...mapGetters(["currentMenu"])
  },
  methods: {
    fetch() {
      if (this.isNew) {
        this.model = {};
        this.loaded = true;
        return;
      }
      this.$http
        .get(this.resourceUri, {
          params: {
            query: {
              with: this.with
            }
          }
        })
        .then(({ data }) => {
          this.loaded = true;
          this.model = data;
        });
    },
    fetchForm() {
      this.$http
        .get(this.formUri, {
          params: this.$route.params
        })
        .then(({ data }) => {
          this.fields = data.fields;
          this.layout = data.layout;
          this.redirect = data.redirect;
          if (data.header) {
            this.header = data.header;
          }
          if (data.tag) {
            this.tag = data.tag;
          }
          this.fetch();
        });
    },

    onSuccess() {
      if (this.redirect === false) {
        this.fetchForm();
      } else if (this.redirect === -1 || !this.redirect) {
        this.$router.go(-1);
      } else {
        this.$router.go(this.redirect);
      }
    }
  },
  mounted() {
    this.site.fetched && this.fetchForm()
  },
  created() {
    // this.fetchForm();
  }
};
</script>

