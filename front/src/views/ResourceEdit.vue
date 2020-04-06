<template>
  <div>
    <b-data-form :resource="resource" :id="id" :languages="$store.state.site.languages"></b-data-form>
  </div>
</template>

<script>
import BDataForm from "../components/DataForm";
export default {
  name: "resource-edit",
  components: {
    BDataForm
  },
  data() {
    return {};
  },
  computed: {
    id() {
      return this.$route.params.id;
    },
    resource() {
      return this.$route.params.resource;
    }
  },
  watch: {},
  methods: {},

  created() {}
};
</script>
