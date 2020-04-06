<template>
  <div>
    <b-data-table v-if="$store.state.site.grid_style == 2" :resource="resource"></b-data-table>
    <custom-table v-else></custom-table>
  </div>
</template>

<script>
import BDataTable from "../components/DataTable";
import CustomTable from "./CustomTable";

export default {
  name: "resource-index",
  components: {
    BDataTable,
    CustomTable
  },
  data() {
    return {};
  },
  computed: {
    resource() {
      return this.$route.params.resource;
    }
  },
  methods: {},
  created() {}
};
</script>
