<script>
// import Chart from "vue-chartjs";

export default {
  // extends: Chart.Pie,
  props: {
    resource: {
      type: String,
      required: true
    },
    group: {
      type: String,
      required: true
    },
    
  },
  data() {
    return {
      options: {}
    };
  },
  computed: {
    resourceUri() {
      return this.resource + "/stat";
    }
  },
  methods: {
    fetch() {
      this.$http.get(this.resourceUri, {
        params: {group: this.group}
      }).then(({ data }) => {
        this.options = data;
        this.renderChart(this.options)
      });
    },
  },
  mounted() {
    // Overwriting base render method with actual data.
    this.fetch()
  }
};
</script>

