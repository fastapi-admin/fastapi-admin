<template>
  <b-table class="table-builder" :fields="fields" :items="items">
    <template v-for="(field, key) in _.omit(fields, '_actions')"  :slot="`HEAD_${key}`">
      <div :key="key" :class="{'text-right': ['number'].includes(field.type)}">
        {{field.label || key}}
      </div>
    </template>
    <template v-for="(field, key) in fields"  :slot="key" slot-scope="row">
      <b-data-value :field="field" :key="key" :lang="currentLanguage" :name="key" :model="row.item" short-id />
    </template>
    
  </b-table>
</template>

<script>
import BDataValue from "./DataValue";
import { mapState, mapGetters } from "vuex";
export default {
  components: {
    BDataValue
  },
  props: {
    fields: {},
    items: Array
  },
  computed: {
    ...mapState(["site", "i18n"]),
    ...mapGetters(["currentMenu", "currentLanguage"]),
  }
}
</script>

