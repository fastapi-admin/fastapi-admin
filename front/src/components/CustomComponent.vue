<template>
  <div>
    <component :is="component" v-if="component"></component>
  </div>
</template>

<script>
export default {
  props: {
    config: {
      required: true
    }
  },
  data(){
    return {
      component: null
    }
  },
  mounted() {

  },
  watch: {
    config: 'setComponent'
  },
  methods: {
    setComponent() {
      if (!this.config) {
        return this.component = null;
      }
      if (typeof this.config === 'string') {
        return this.component = {
          template: this.config
        }
      }
      const component = {};
      const config = this.config;
      const rawData = Object.assign({}, config.data);
      component.data = rawData;
      component.name = config.name
      if (typeof component.data !== "function") {
        component.data = function() {
          return Object.assign({}, rawData);
        };
      }
      const wrapFunction = v => {
        if (Array.isArray(v)) {
          return new Function(...v);
        }
        return v;
      };
      const mapValues = (obj = {}) => {
        return Object.entries(obj).reduce((acc, [k, v]) => {
          acc[k] = wrapFunction(v);
          return acc;
        }, {});
      };

      component.methods = mapValues(config.methods, wrapFunction);
      component.computed = mapValues(config.computed, wrapFunction);
      component.created = config.created ? wrapFunction(config.created) : null;
      component.mounted = config.mounted ? wrapFunction(config.mounted) : null;
      component.watch = config.watch ? wrapFunction(config.watch) : null;
      component.template = config.template
      component.render = wrapFunction(config.render)
      this.component = Object.assign({}, component, {});
    }
  }
};
</script>

