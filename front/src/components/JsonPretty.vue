<template>
  <div>
    <vue-json-pretty
      :data=value
      :highlightMouseoverNode="true"
    >
    </vue-json-pretty>
  </div>
</template>
<script>
  import VueJsonPretty from 'vue-json-pretty'

  export default {
    name: "b-json-pretty",
    components: {
      VueJsonPretty
    },
    props: {
      value: null,
    },
  }
</script>


