<template>
  <v-select
    v-model="model"
    @search="getAjaxOptions"
    label="text"
    :options="newOptions"
    :multiple="multiple"
  >
    <div slot="no-options">{{noOptionsText}}</div>
  </v-select>
</template>

<script>
import VSelect from "vue-select";

export default {
  components: {
    VSelect
  },
  data() {
    return {
      newOptions: this.options.slice(0),
      q: ""
    };
  },
  props: {
    value: {
      deafult() {
        return this.multiple ? [] : null;
      }
    },
    options: {
      default: () => []
    },
    name: {},
    multiple: {},
    field: {},
    parent: {},
    ajaxOptions: {},
    noOptionsText: {
      default() {
        return this.$t("messages.no_options_text");
      }
    }
  },
  computed: {
    model: {
      get() {
        if (this.multiple) {
          return this.newOptions.filter(v => this.value.includes(v.value));
        } else {
          return this.newOptions.find(v => this.value === v.value);
        }
      },
      set(val) {
        if (val === null || val.value === null) {
          return this.$emit("input", null);
        }
        let ret;
        if (this.multiple) {
          const isChanged = JSON.stringify(val) !== JSON.stringify(this.value);
          if (isChanged) {
            ret = val.map(v => v.value);
          }
        } else {
          ret = val.value;
        }
        if (ret !== null) {
          this.$emit("input", ret);
        }
      }
    }
  },
  methods: {
    getAjaxOptions(q) {
      this.q = q;
      this.fetchOptions();
    },
    initOptionsForSelect2() {
      const parentOptions = this.parent[this.name + "_data"];
      if (parentOptions) {
        this.newOptions = this.options.concat(parentOptions);
      }
    },
    fetchOptions(query = {}) {
      const params = this.ajaxOptions;
      const { url, resource, where = {}, text, depends } = params;
      params.where = Object.assign({}, where, query);
      if (this.q) {
        params.q = this.q;
      }
      const apiUrl = url
        ? _.template(url)({ item: this.parent })
        : resource + "/options";
      this.$http.get(apiUrl, { params }).then(({ data }) => {
        this.model = { value: null };
        this.newOptions = data;
      });
    }
  },
  mounted() {
    if (this.ajaxOptions) {
      const { url, resource, where, depends } = this.ajaxOptions;
      if (depends) {
        this.$watch(
          `parent.${depends}`,
          val => {
            // console.log(val);
            this.fetchOptions({ [depends]: val });
          },
          {
            // deep: true,
            immediate: true
          }
        );
      } else {
        this.fetchOptions();
      }
    }
  }
};
</script>

