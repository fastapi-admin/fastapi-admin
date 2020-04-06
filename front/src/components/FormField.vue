<template>
  <div>
    <div class="languages mb-1" v-if="isIntl">
      <span
        class="badge mr-1 mb-0 pointer"
        :class="`badge-${currentLanguage === key ? 'primary' : 'secondary'}`"
        v-for="(lang, key) in languages"
        :key="key"
        @click="changeLanguage(key, name)"
      >{{lang}}</span>
    </div>
    <b-form-select
      v-if="['select'].includes(field.type)"
      :formatter="getFormatter(field, value)"
      :id="id"
      :options="options"
      v-bind="field"
      v-model="model"
      
      :name="name"
    ></b-form-select>
    <div v-else-if="['select2'].includes(field.type)">
      <b-select v-model="model" v-bind="field" :parent="parent"></b-select>
    </div>
    <b-tree-select
      :normalizer="treeSelectNormalizer"
      value-consists-of="LEAF_PRIORITY"
      v-else-if="['tree', 'treeselect'].includes(field.type)"
      v-bind="field"
      v-model="model"
    />
    <!-- <b-select v-if="['select', 'select2'].includes(field.type)" track-by="value" label="text" @input="model = arguments[0]" :id="id" v-bind="field" :title="value" /> -->

    <b-date-picker
      v-else-if="['date', 'datetime'].includes(field.type)"
      :name="name"
      v-bind="field"
      v-model="model"
    />
    <b-form-radio-group
      v-else-if="['radiolist'].includes(field.type)"
      :name="name"
      v-bind="field"
      v-model="model"
    >
      <!-- <b-form-radio :key="choice.value" :value="choice.value" v-for="choice in field.options">{{choice.text}}</b-form-radio> -->
    </b-form-radio-group>
    <b-form-checkbox-group
      :name="name"
      v-else-if="['checkboxlist'].includes(field.type)"
      v-bind="field"
      v-model="model"
    >
      <!-- <b-form-checkbox :key="choice.value" :value="choice.value" v-for="choice in field.options">{{choice.text}}</b-form-checkbox> -->
    </b-form-checkbox-group>
    <div v-else-if="['checkboxtable'].includes(field.type)" class="checkboxtable">
      <div v-for="(options, group) in groupedOptions" :key="group" class="mt-1">
        <b-form-checkbox-group :name="name" :options="options" v-bind="field" v-model="model"></b-form-checkbox-group>
      </div>
    </div>
    <b-form-textarea
      :name="name"
      v-else-if="['textarea'].includes(field.type)"
      :id="id"
      v-model="model"
      v-bind="field"
      :rows="field.rows || 3"
    />
    <div v-else-if="['file-picker'].includes(field.type)">
      <b-btn v-b-modal.file-manager>选择文件</b-btn>
    </div>
    <!-- <b-uploader v-else-if="['image', 'file', 'audio'].includes(field.type)" :id="id" v-model="model" v-bind="field" /> -->

    <component
      :is="field.autoUpload === false ? 'b-form-file' : 'b-form-uploader'"
      v-else-if="['image', 'file', 'audio', 'video'].includes(field.type)"
      :field="field"
      v-model="model"
      :id="id"
      :name="name"
      :parent="parent"
    />
    <div v-else-if="['switch', 'checkbox'].includes(field.type)">
      <b-form-checkbox
        variant="success"
        v-bind="field"
        size="lg"
        pill
        type="3d"
        :id="id"
        v-model="model"
      />
    </div>
    <!-- <b-ueditor :state="state" v-else-if="['wysiwyg', 'html'].includes(field.type)" :id="id" v-bind="field" v-model="model" /> -->

    <div v-else-if="['wysiwyg', 'html'].includes(field.type)">
      <!-- <b-btn :id="`cropper_${id}`" variant="success">图片裁剪助手</b-btn> -->
      <avatar-cropper
        v-if="field.cropper"
        :trigger="`#cropper_${id}`"
        v-bind="cropperOptions"
        ref="cropper"
        @uploaded="cropperUploaded"
        @completed="cropperUploadComplete"
      />
      <b-html-editor
        ref="editor"
        :state="state"
        :id="id"
        v-bind="field"
        v-model="model"
        :content="model"
        @open-cropper="$refs.cropper && $refs.cropper.pickImage()"
        @change="htmlEditorInput"
        @keyup.native.enter="wrapFirstLine"
      />
      <!-- <b-cropper v-if="field.showCropper" ref="cropper" ></b-cropper> -->
    </div>
    <div v-else-if="['json'].includes(field.type)">
      <b-form-textarea :id="id" v-model="model" v-bind="field" :rows="field.rows || 5"/>
      <!-- <v-jsoneditor v-if="model" :value="JSON.parse(model)" 
     @input="model = JSON.stringify(arguments[0])"
      :options="{}" />-->
    </div>
    <div v-else-if="field.fields">
      <div v-if="['array'].includes(field.type) || field.is_array || parent.is_array">
        <b-table
          hover
          bordered
          :items="model"
          :fields="myFields"
          v-if="field.is_table || parent.is_table"
        >
          <template v-for="(child, k) in myFields" :slot="k" slot-scope="row">
            <b-form-field
              :parent="parent"
              v-model="model[row.index][k]"
              :field="child"
              :name="`input_${row.index}_${k}`"
              :key="`input_${row.index}_${k}`"
              :id="`input_${row.index}_${k}`"
            />
          </template>
          <template slot="HEAD__actions">
            <b-btn size="sm" @click="addRow">
              <i class="icon-plus"></i>
              {{$t('actions.add')}}
            </b-btn>
          </template>
          <template slot="_actions" slot-scope="row">
            <b-btn size="sm" @click="model.splice(row.index + 1, 0, {});">
              <i class="icon-plus"></i>
              {{$t('actions.add')}}
            </b-btn>
            <b-btn size="sm" @click="model.splice(row.index, 1);">
              <i class="icon-trash"></i>
              {{$t('actions.delete')}}
            </b-btn>
          </template>
        </b-table>
        <b-draggable v-model="model" v-else>
          <transition-group tag="div" class="row">
            <b-col
              v-for="(item, i) in model"
              :key="`draggable-${name}-${i}`"
              cols
              :lg="field.item_cols || 6"
            >
              <b-card class="mb-4">
                <b-row slot="header" class="justify-content-between">
                  <b-col>No. {{i + 1}}</b-col>
                  <b-col right class="text-right">
                    <b-btn size="sm" @click="model.splice(i, 1)">
                      <i class="icon-trash"></i>
                      {{$t('actions.delete')}}
                    </b-btn>
                  </b-col>
                </b-row>
                <b-form-group
                  v-for="(child, key) in myFields"
                  :key="key"
                  v-bind="child"
                  :label-for="`input_${name}_${i}_${key}`"
                >
                  <b-form-field
                    v-model="model[i][key]"
                    :parent="parent"
                    :name="`${name}.${i}.${key}`"
                    :field="child"
                    :id="`input_${name}_${i}_${key}`"
                  />
                </b-form-group>
              </b-card>
            </b-col>
            <b-col
              cols
              :lg="field.item_cols || 6"
              :key="-1"
              class="d-flex align-items-center justify-content-center"
            >
              <b-btn
                size="lg"
                class="p-5"
                block
                @click="model = !model? [] : model; model.push({})"
              >
                <i class="fa fa-plus"></i>
              </b-btn>
            </b-col>
          </transition-group>
        </b-draggable>
      </div>
      <div v-else-if="['object'].includes(field.type)">
        <b-card>
          <b-form-builder
            :sub-form="name || ''"
            v-model="model"
            :languages="languages"
            :fields="myFields"
            :parent="parent"
            ref="subForm"
          ></b-form-builder>
          <!-- <b-form-group v-for="(child, key) in myFields" :key="key" v-bind="child" :label-for="`input_${name}_${key}`">
          
          <b-form-field :value="_.get(model, `${key}`)"
          @input="model[key] = arguments[0]"
          :parent="parent" :name="`${name}_${key}`" :field="child" :id="`input_${name}_${key}`" />
          </b-form-group>-->
        </b-card>
      </div>
      <div v-else>
        <b-form-group
          v-for="(child, key) in myFields"
          :key="key"
          v-bind="child"
          :label-for="`input_${name}_${key}`"
        >
          <b-form-field
            v-model="model[key]"
            :parent="parent"
            :name="key"
            :field="child"
            :id="`input_${name}_${key}`"
          />
        </b-form-group>
      </div>
    </div>
    <b-input-group v-else>
      <b-input-group-prepend is-text v-if="field.prependIcon || field.prepend">
        <i :class="field.prependIcon" v-if="field.prependIcon"></i>
        <span v-else v-html="field.prepend"></span>
      </b-input-group-prepend>
      <b-form-input
        :state="state"
        :id="id"
        :name="name"
        v-bind="field"
        v-model="model"
        :formatter="getFormatter(field, value)"
      />
      <b-input-group-append is-text v-if="field.appendIcon || field.append">
        <i :class="field.appendIcon" v-if="field.appendIcon"></i>
        <span v-else v-html="field.append"></span>
      </b-input-group-append>
    </b-input-group>
  </div>
</template>
<style>
.checkboxtable .btn-group > .btn:first-child {
  text-align: center;
  width: 10em;
  margin-right: 2px;
}
.vue-html5-editor .content {
  max-height: 500px;
}
</style>

<script>
import Vue from "vue";
import BDraggable from "vuedraggable";
import BTreeSelect from "@riophae/vue-treeselect";
import "@riophae/vue-treeselect/dist/vue-treeselect.min.css";
// import BSelect from "vue-multiselect"
import BSelect from "./FormSelect2";
// import BSelect from "@alfsnd/vue-bootstrap-select";
// import "vue-multiselect/dist/vue-multiselect.min.css"
import BDatePicker from "vue2-datepicker";
// import BUeditor from "./UEditor"
import BFormUploader from "./FormUploader";
import VueHtml5Editor from "vue-html5-editor";
// import BJsonEditor  from "./JsonEditor"
// import BJsonEditor from "vue-jsoneditor"
import _ from "lodash";

// import "jsoneditor/dist/jsoneditor.min.css"

// Vue.use(BJsonEditor);
export default {
  components: {
    // BUeditor,
    BDatePicker,
    BSelect,
    BFormUploader,
    // BJsonEditor,
    BDraggable,
    BTreeSelect
  },
  props: {
    languages: {},
    id: {
      required: true
    },
    parent: {},
    value: {},
    field: {},
    state: {},
    name: {}
  },
  computed: {
    cropperOptions() {
      return {
        "upload-url": global.API_URI + "upload",
        "upload-headers": {
          Authorization: "Bearer " + this.$store.state.auth.token
        },
        "upload-form-name": "file",
        "upload-form-data": {
          from: "cropper"
        },
        "cropper-options": {
          viewMode: 2,
          aspectRatio: _.get(this.field, "cropper.ratio", 1)
        },
        "output-options": this.field.cropper,
        labels: this.field.labels || { submit: "提交", cancel: "取消" }
      };
    },
    isSelect() {
      return ["select", "select2"].includes(this.field.type);
    },
    isSelect2() {
      return ["select2"].includes(this.field.type);
    },
    groupedOptions() {
      return _.groupBy(this.options, "group");
    },
    myFields() {
      let fields = this.field.fields;
      if (typeof fields == "string") {
        const rel = this.parent[fields];
        if (!rel) {
          return {};
        }
        try {
          fields = JSON.parse(rel);
        } catch (e) {
          fields = {};
        }
      }
      if (this.parent.is_table) {
        fields._actions = { label: this.$t("actions.actions") };
      }

      return fields;
    },
    description() {
      if (this.field.limit) {
        const { width, height } = this.field.limit;
        if (width && height) {
          return `尺寸：${width}x${height}`;
        }
        return;
      }
      return this.field.description;
    },
    filteredValue() {
      let defaultValue = this.value;
      if (!this.defaultValue) {
        if (["object", "json"].includes(this.field.type)) {
          defaultValue = {};
        }
        if (["array"].includes(this.field.type) || this.field.multiple) {
          defaultValue = [];
        }
      }
      // console.log(defaultValue);
      return defaultValue;
    },
    isArrayValue() {
      return (
        this.field.multiple ||
        this.field.is_array ||
        this.field.type == "array" ||
        this.field.is_table
      );
    },
    isIntl() {
      return this.field.intl || this.field.multilingual;
    },
    selectedValue1() {
      let value = this.initSelectedValue
      if (this.isArrayValue) {
        value = _.filter(
          this.options,
          v => this.value && this.value.includes(v.value)
        );
      } else {
        value = _.find(this.options, v => this.value == v.value);
      }
      return value;
    },
    model: {
      get() {
        const isArray =
          this.field.multiple ||
          this.field.is_array ||
          this.field.type == "array" ||
          this.field.is_table;
        const isObject = this.field.type == "object";
        let ret = this.value;
        if (!this.value) {
          if (isArray) {
            ret = [];
          } else if (isObject) {
            ret = {};
          }
        }
        if (this.isIntl) {
          // console.log(this.name, ret, this.currentLanguage);
          return _.get(ret, this.currentLanguage, "");
        }
        return ret;
      },
      set(value) {
        this.$emit("input", value, this.currentLanguage);
      }
    }
  },
  data() {
    const isArray =
      this.field.multiple ||
      this.field.is_array ||
      this.field.type == "array" ||
      this.field.is_table;
    return {
      currentLanguage: this.field.currentLanguage || "en",
      options: this.field.options || [],
      initSelectedValue: isArray && !this.value ? [] : this.value,
      selectedValue: isArray && !this.value ? [] : this.value,
    };
  },
  methods: {
    addRow() {
      if (!this.parent[this.name]) {
        this.$set(this.parent, this.name, []);
      }
      this.$nextTick(() => {
        this.model.push({});
      });
    },
    initEditor() {
      const language = "zh-cn";
      window.document.execCommand("defaultParagraphSeparator", false, "p");

      const visibleModules = this.field.modules || [
        "text",
        // "color",
        // "font",
        "heading",
        "align",
        "list",
        "link",
        "unlink",
        "tabulation",
        "image",
        // this.field.cropper ? "cropper" : "image",
        "hr",
        "eraser",
        "undo",
        "full-screen",
        "cropper"

        // "info",
      ];
      const cropperClass = _.get(
        this.field,
        "cropper.icon",
        "fa fa-crop text-danger"
      );

      Vue.use(VueHtml5Editor, {
        name: "b-html-editor",
        language,
        showModuleName: false,
        modules: [
          {
            name: "cropper",
            icon: cropperClass,
            i18n: "cropper",
            show: true,
            handler: function(editor) {
              editor.$emit("open-cropper");
            }
          },
          {
            name: "heading",
            icon: "fa fa-header",
            i18n: "heading",
            show: true,
            dashboard: {
              template: `
                <div>
                  <button v-for="h in 6" type="button" @click="setHeading(h)">H{{h}}</button>
                </div>
              `,
              methods: {
                setHeading(heading) {
                  this.$parent.execCommand("formatBlock", `h${heading}`);
                }
              }
            }
          }
        ],
        i18n: {
          "zh-cn": {
            cropper: "图片裁剪",
            heading: "标题"
          }
        },
        image: {
          sizeLimit: 10 * 1024 * 1024,
          upload: {
            url: global.API_URI + "upload",
            headers: {
              Authorization: "Bearer " + this.$store.state.auth.token
            },
            fieldName: "file"
          },
          // compress: {
          //   width: 1600,
          //   height: 1600,
          //   quality: 80
          // },
          uploadHandler(res) {
            let data;
            try {
              data = JSON.parse(res);
            } catch (e) {
              this.$notify.error("上传失败");
            }
            return data.url;
          }
        },
        visibleModules: visibleModules
      });
    },
    cropperUploaded(res) {
      this.$refs.editor.execCommand("insertHTML", `<img src="${res.url}" />`);
    },
    cropperUploadComplete(data) {
      if (data.message) {
        this.$snotify.error(data.message);
      }
    },
    changeLanguage(lang) {
      this.currentLanguage = lang;
      // this.$emit('change-language', lang, name)
      // global.console.log(lang, name)
    },
    htmlEditorInput(value) {
      this.$emit("input", value, this.currentLanguage);
    },
    wrapFirstLine() {
      // const value = String(el.target.innerHTML).replace(/^\s*(.+?)(<?)/i, '<p> $1 </p>$2')
      // this.$emit('input', value)
    },
    treeSelectNormalizer(row) {
      return {
        id: row.value,
        label: row.text
      };
    },
    getFormatter(field) {
      if (field.format) {
        return eval(field.format);
      }
      return v => v;
    },

    fetchAjaxOptions(query = {}) {
      const params = this.field.ajaxOptions;
      const { url, resource, where = {}, text, depends } = params;
      params.where = Object.assign({}, where, query);
      if (this.q) {
        params.q = this.q;
      }
      const apiUrl = url
        ? _.template(url)({ item: this.parent })
        : resource + "/options";
      this.$http.get(apiUrl, { params }).then(({ data }) => {
        this.options = data;
      });
    }
  },
  mounted() {
    if (this.field.type == "html") {
      // window.onscroll =  () => {
      //   const editor = this.$refs.editor.$el
      //   const offsetTop = editor.getClientRects()[0].top
      //   // const scrollTop = document.documentElement.scrollTop
      //   if (offsetTop <= 0) {
      //     editor.classList.toggle()
      //   }
      //   // global.console.log(scrollTop, offsetTop)
      // }
    }
  },
  created() {
    if (this.field.type == "html") {
      this.initEditor();
    }
    if (this.field.ajaxOptions && this.field.ajaxOptions.search !== true) {
      this.fetchAjaxOptions();
    }
    if (this.isSelect2) {
      // this.initOptionsForSelect2();

      // this.$watch("options", () => {

      // });
    }
  }
};
</script>
