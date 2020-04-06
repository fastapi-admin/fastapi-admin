<template>
  <div class="app login-container" :style="site.login_style">
    <div class="col-md-7 mt-5">
      <div class="card-group">
        <div class="card p-4">
          <div class="card-body">
            <h1>{{$t('actions.login')}}</h1>
            <img :src="site.login_logo" style="margin-bottom:20px">
            <p class="text-muted">{{$t('messages.login_please')}}</p>
            <b-form-builder
              action="login"
              :fields="fields"
              v-model="model"
              @success="onSuccess"
              :submitText="$t('actions.login')"
              backText
            />
          </div>
        </div>
        <div class="card text-white bg-primary py-5 d-md-down-none" :style="site.desbg_style">
          <div class="card-body text-center align-items-center d-flex">
            <div class style="width: 100%">
              <h2>{{site.name || 'REST ADMIN'}} - {{$t('messages.dashboard')}}</h2>
              <p>{{site.description || $t('messages.login_description')}}</p>
              <!-- <button type="button" class="btn btn-primary active mt-3">{{$t('messages.go_home')}}</button> -->
            </div>
          </div>
        </div>
      </div>

      <p class="text-muted m-4 text-center">{{site.login_footer || $t('messages.login_footer')}}</p>
      <locale-switcher class="text-center"></locale-switcher>
    </div>
  </div>
</template>

<script>
import { types } from "../store";
import { mapState } from "vuex";
import LocaleSwitcher from "../components/LocaleSwitcher";

export default {
  name: "Login",
  components: { LocaleSwitcher },
  computed: {
    ...mapState(["auth", "site"]),
    fields() {
      return {
        username: {
          label: this.$t("fields.username"),
          placeholder: this.$t("fields.username"),
          icon: "icon-user"
        },
        password: {
          label: this.$t("fields.password"),
          placeholder: this.$t("fields.password"),
          icon: "icon-lock",
          type: "password"
        }
      };
    }
  },
  data() {
    return {
      model: {
        username: "",
        password: ""
      },
      errors: []
    };
  },
  methods: {
    onSuccess(data) {
      this.$store.commit(types.SET_AUTH, data);
      this.$store.dispatch(types.FETCH_SITE);
      this.$router.push({
        path: data.redirect || "/"
      });
    }
  },
  mounted() {}
};
</script>

<style lang="scss">
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
}
</style>
