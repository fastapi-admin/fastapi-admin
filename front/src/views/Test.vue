<template>
  <div>
    <b-form-select v-model="cat" :options="options"></b-form-select>
    <b-form-selectx v-model="cat" :options="options" ></b-form-selectx>
  </div>
</template>
<script>
import BFormSelectx from "../components/FormSelect";
export default {
  components: { BFormSelectx },
  data(){
    return {
      cat: 0,
      options: 'html css nodejs'.split(' ').map(v => ({text: v.toUpperCase(), value: v, html: `<b>${v}</b>`}))
    }
  }
};
</script>

