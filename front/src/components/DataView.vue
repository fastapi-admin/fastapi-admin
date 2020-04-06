<template>
  <div class="page-view">
    <div class="data-view">
      <legend v-if="model[$config.primaryKey]">{{$t('actions.view')}}: {{model[$config.primaryKey]}}</legend>
      <table class="table ">
        <tbody>
          <tr v-for="(field, key) in fields" :key="key">
            <th style="min-width:120px">{{field.label || key}}</th>
            <td>
              <div v-if="['array'].includes(field.type)">
                <b-table :items="model[key]" :fields="field.fields">
                  <template v-for="(child, k) in field.fields" :slot="k" slot-scope="row">
                    <b-data-value :lang="currentLanguage" :field="child" :name="k" :key="k" :model="row.item" />
                  </template>
                </b-table>
              </div>
              <div v-else>
                <b-data-value :lang="currentLanguage" :field="field" :name="key" :model="model" />
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div slot="footer">
      <b-btn @click="$router.go(-1)">{{$t('actions.back')}}</b-btn>
    </div>
  </div>
</template>

<script>
import BDataValue from "./DataValue";
import _ from 'lodash'

import { mapState, mapGetters } from 'vuex'
export default {
  components: {
    BDataValue
  },
  props: {
    resource: {
      type: String,
      required: true
    },
    id: {
      default: '',
      required: true
    },
    viewPath: {
      type: String,
      default: "view",
      required: false
    },

  },
  data() {
    return {
      choices: {},
      fields: {},
      model: {},
      errors: [],
      items: []
    };
  },

  computed: {
    resourceUri() {
      let url = [this.site.resource_prefix, this.resource, this.id]
        .filter(v => v)
        .join("/");
      return url;
    },
    viewUri() {
      let url = [this.site.resource_prefix, this.resource, this.viewPath]
        .filter(v => v)
        .join("/");
      url += "?id=" + (this.id || "");
      return url;
    },
    with() {
      return _.filter(
        _.map(this.fields, (v) => v.ref && v.ref.replace(/\.\w+$/, ''))
      );
    },

    ...mapState(['site']),
    ...mapGetters(["currentMenu", "currentLanguage"]),
    header() {
      return `
        ''
        <small> ${this.resource.toUpperCase()} </small>
      `
    },
  },
  methods: {
    fetch() {
      this.$http.get(this.resourceUri, {
        params: {
          query: { with: this.with }
        }
      }).then(({ data }) => {
        this.model = data;
      });
    },
    fetchView() {
      this.$http.get(this.viewUri).then(({ data }) => {
        this.fields = data.fields;
        delete this.fields._actions
        this.fetch();
      });
    },
  },
  watch: {
    id: "fetchForm",
    "site.fetched"(val){
      if (val) {
        this.fetchView(true)
      }
    },
  },
  mounted() {

  },
  created() {
    this.site.fetched && this.fetchView();


  }
};
</script>

