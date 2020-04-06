<template>
  <div>
    <b-card>
      <b-data-value class="text-center" :field="field" :name="name" :model="parent"/>
      <div
        class="text-center text-muted mt-2"
        v-if="field.limit && field.limit.width"
      >{{$t('messages.image_size', field.limit)}}</div>
      <div slot="footer" class="text-center">
        <b-form-file
          ref="file"
          :id="fileName"
          :name="name"
          v-model="file"
          v-bind="field"
          @input="upload"
          class="d-none"
          :multiple="false"
        />
        <b-form-input
          :value="String(file || '')"
          @input="$emit('input', arguments[0])"
          v-if="field.showInput"
          class="mb-2"
        ></b-form-input>
        <b-btn
          v-if="field.showBrowse"
          @click="$emit('open-file-browser')"
          class="mr-2"
          size="sm"
        >{{$t('actions.file_browser')}}</b-btn>
        <label
          :for="`file_${id}`"
          class="btn btn-primary m-0 mr-2 btn-sm"
        >{{file ? $t('actions.change') : $t('actions.choose')}}</label>
        <b-btn @click="$emit('remove')" class="mr-2" size="sm">{{$t('actions.delete')}}</b-btn>
        <b-btn @click="$emit('add')" v-if="allowAdd" class="mr-2" size="sm">{{$t('actions.add')}}</b-btn>
        <b-btn
          v-if="field.showCopy"
          ref="copy_btn"
          :data-clipboard-text="value"
          class="mr-2"
          size="sm"
        >{{$t('actions.copy')}}</b-btn>
      </div>
    </b-card>
  </div>
</template>
<script>
// import ClipboardJS from 'clipboard'
import BDataValue from "./DataValue";
import Vue from "vue";

export default {
  components: {
    BDataValue
  },
  props: {
    value: {},
    field: {},
    id: {},
    parent: {},
    name: {},
    allowAdd: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      model: this.value,
      file: this.value,
      current: this.value,
      fileData: {}
    };
  },
  watch: {
    value(val) {
      this.file = val;
    }
  },
  computed: {
    text() {
      return String(this.value)
        .split("/")
        .pop();
    },
    modalName() {
      return `modal_${this.id}`;
    },
    fileName() {
      return `file_${this.id}`;
    },
    tag() {
      const tags = {
        image: "img",
        audio: "audio",
        video: "video"
      };
      return tags[this.field.type] ? tags[this.field.type] : "div";
    }
  },
  mounted() {
    Vue.nextTick(() => {
      // new ClipboardJS(this.$refs.copy_btn)
    });
  },
  methods: {
    reset(error) {
      if (error) {
        this.$snotify.error(error);
      }
      this.model = this.oldValue;
      return false;
    },
    upload() {
      if (!this.file) {
        return;
      }
      const fd = new FormData();
      fd.append("type", this.name);
      fd.append("file", this.file);
      this.fileData = this.file;

      const src = URL.createObjectURL(this.file);

      const doUpload = () => {
        this.$http.post("upload", fd).then(({ data }) => {
          this.file = data.url;
          this.$emit("input", this.file);
          this.$snotify.success(this.$t("messages.uploaded"));
        });
      };

      const { width, height, size } = this.field.limit || {};

      if (this.file.size > size) {
        return this.reset(
          this.$t("errors.too_large", { limit: parseInt(size / 1024) })
        );
      }

      if (this.file.type.match(/^image/)) {
        let file = new Image();
        file.src = src;
        file.onload = () => {
          if (this.field.limit) {
            if (file.naturalHeight != height || file.naturalWidth != width) {
              return this.reset(
                this.$t("errors.wrong_size", { width, height })
              );
            }
          }
          doUpload();
        };
      } else {
        doUpload();
      }
    }
  }
};
</script>

<style scoped>
.current {
  border: 1px solid #c30;
}
.item {
  max-width: 100%;
  max-height: 200px;
}
</style>

