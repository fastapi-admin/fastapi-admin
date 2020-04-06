<template>
  <b-card :header="form.header">
    <div class="custom-form">
      <div class="row">
        <div class="col col-md-8">
          <legend>{{form.title}}</legend>
        </div>
        <div class="col col-md-4 text-right hidden-sm-down">
          <b-btn @click="$router.go(-1)">{{$t('actions.back')}}</b-btn>
          <b-btn variant="primary" @click="$refs.form.handleSubmit()">{{form.submitText || $t('actions.save')}}</b-btn>
        </div>
      </div>
      <b-form-builder v-if="form.fields" ref="form" v-bind="form" @success="onSuccess" :auth="auth" />
    </div>
  </b-card>
</template>

<script>
import { mapState } from "vuex";

export default {
  components: {},
  props: {
    
    
  },
  data() {
    return {
      loaded: false,
      form: {}
    };
  },
  watch: {
    '$route'(){
      this.fetchForm()
    }
  },
  computed: {
    ...mapState(["auth"]),
    uri(){
      return this.$route.params.uri.replace(/\./g, '/')
    }
  },
  methods: {
    fetch() {
      
    },
    fetchForm() {
      this.$http.get(this.uri).then(({ data }) => {
        this.form = data;
        if (!this.form.action) {
          this.form.action = this.uri
        }
        if (!this.form.title) {
          this.form.title = this.$inflection.titleize(String(this.$route.query.uri).split('/').pop())
        }
        // this.fetch();
      });
    },

    onSuccess(data) {
      const {message, then, redirect} = data
      if (message) {
        this.$snotify.success(message);
      }
      if (then) {
        eval(then)
      } else if (redirect) {
        this.$router.push({path: redirect})
      } else {
        // this.$router.go(-1);
      }
    }
  },
  mounted() {},
  created() {
    this.fetchForm();
  }
};
</script>

