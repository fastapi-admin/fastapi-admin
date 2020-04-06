<template>
  <div ref="editor"></div>
</template>
<script>
import 'jsoneditor/dist/jsoneditor.min.css'
import JSONEditor from "jsoneditor";
export default {
  name: "b-json-editor",
  props: {
    value: null,
    options: {}
  },
  data() {
    return {
      editor: null
    };
  },
  mounted() {
    this.editor = new JSONEditor(this.$refs.editor, this.options);
    if (typeof this.value === "string") {
      this.value = JSON.parse(this.value);
    }
    this.editor.set(this.value || {});
    this.editor.onChange = v => {
      this.$emit("input", JSON.stringify(v));
    };
  },
  created() {}
};
</script>
