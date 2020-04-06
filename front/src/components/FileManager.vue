<template>
  <b-modal id="file-manager" title="文件管理器">
    <b-table :items="items" :fields="fields">
      <b-data-value slot-scope="data" slot="url" name="url" :model="data.item" :field="fields.url"></b-data-value>
    </b-table>
  </b-modal>
</template>

<script>
import { mapState } from "vuex";
export default {
  data() {
    return {
      fields: {
        originalname: { label: "原文件名" },
        url: { type: "image", style: { height: "3em" } }
      },
      items: []
    };
  },
  computed: {
    ...mapState(["site"]),
    fileUrl() {
      return [this.site.resource_prefix, "files"].filter(v => v).join("/");
    }
  },
  watch: {
    "site.fetched": "fetch"
  },
  methods: {
    fetch() {
      this.$http.get(this.fileUrl).then(({ data }) => {
        this.items = data.data;
      });
    }
  },
  created() {
    this.site.fetched && this.fetch();
  }
};
</script>

