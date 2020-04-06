<template>
  <b-dropdown split variant="primary" no-caret1 class="selectx">
    <template slot="button-content">
      <span>
        {{model}}
        <!-- <b-btn-close></b-btn-close> -->
      </span>
      <!-- <b-form-input class="border-0 w-auto d-inline-block" v-model="q"></b-form-input> -->
    </template>
    <b-dropdown-item-button
      @click="choose(item)"
      v-for="item in options"
      :key="item.value"
      :active="getIsActive(item)"
    >{{item.text}}</b-dropdown-item-button>
    <!-- <b-dropdown-item>Second Action</b-dropdown-item>
    <b-dropdown-item>Third Action</b-dropdown-item>
    <b-dropdown-divider></b-dropdown-divider>
    <b-dropdown-item active>Active action</b-dropdown-item>
    <b-dropdown-item disabled>Disabled action</b-dropdown-item>-->
  </b-dropdown>
</template>

<script>
export default {
  props: {
    value: {},
    options: {},
    multiple: { type: Boolean }
  },
  data() {
    return {
      q: ""
    };
  },
  methods: {
    getIsActive(item) {
      if (this.multiple) {
        return (this.model || []).includes(item.value);
      } else {
        return this.model === item.value;
      }
    },
    choose(item) {
      const val = item.value;
      if (this.multiple) {
        let values = this.model.slice(0);
        const i = values.findIndex(val);
        // console.log(i);
        if (i) {
          values.splice(i, 1);
        } else {
          values.push(val);
        }
        return this.$emit("input", values);
      }
      this.$emit("input", val);
    }
  },
  computed: {
    values() {},
    model: {
      get() {
        if (this.multiple && !this.value) {
          return [];
        }
        const selected = this.options.find(v => v.value === this.value)
        return selected ? selected.text : null;
      },
      set(val) {
        if (this.multiple) {
          let values = this.model.slice(0);
          const i = values.findIndex(val);
          if (i) {
            values.splice(i, 1);
          } else {
            values.push(val);
          }
          return this.$emit("input", values);
        }
        this.$emit("input", val);
      }
    }
  }
};
</script>

<style>
.selectx{
  /* min-width:15em; */
  /* text-align: left; */
}
</style>
