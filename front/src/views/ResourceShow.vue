<template>
  <div >
    <b-row>
      <b-col cols="12" xl="12">
       
          <b-data-view :resource="resource" :id="id"></b-data-view>
        
      </b-col>
    </b-row>
  </div>
</template>

<script>
import BDataView from '../components/DataView'
export default {
  components: {
    BDataView
  },
  data() {
    return {

    };
  },
  computed: {
    id() {
      return this.$route.params.id
    },
    resource() {
      return this.$route.params.resource
    }
  },
  methods: {
    
  },
  created() {
    
  }
};
</script>
