<template>
  <div class="data-table">
    <div v-if="site.grid_style === 1">
      <div class="pb-3">
        <b-btn
          class="mr-2"
          :to="'/rest/' + resourceUri + '/create'"
          variant="secondary"
          v-if="_.get(actions,'toolbar.create') !== false"
        >
          <i class="icon-plus"></i>
          {{$t('actions.create')}}
        </b-btn>
        <b-btn
          class="mr-2"
          @click="fetchGrid"
          variant="success"
          v-if="_.get(actions, 'toolbar.reload') !== false"
        >
          <i class="icon-reload"></i>
          {{$t('actions.reload')}}
        </b-btn>
        <b-btn
          class="mr-2"
          v-for="button in _.get(actions, 'toolbar.extra', [])"
          :key="button.label"
          v-bind="button"
        >{{button.label}}</b-btn>
        <b-btn
          @click="removeAll"
          class="pull-right"
          variant="second"
          v-if="_.get(actions, 'toolbar.delete_all') === true"
        >
          <i class="icon-trash"></i>
          {{$t('actions.delete_all')}}
        </b-btn>
      </div>
      <div class="mb-2 data-table-search" v-if="!_.isEmpty(searchFields)">
        <b-form-builder
          :inline="true"
          :fields="searchFields"
          :action="searchUri"
          v-model="searchModel"
          :submitText="$t('actions.search')"
          backText
          method="get"
          :on-submit="onSearch"
        >
          <div slot="extra-buttons" class="ml-2">
            <b-button
              type="button"
              @click="searchAndExport"
              variant="success"
              v-if="_.get(actions, 'export')"
            >{{$t('actions.search_and_export')}}</b-button>
            <iframe :src="iframeSrc" style="width:0;height:0;border:none;"></iframe>
          </div>
        </b-form-builder>
      </div>
      <div class v-if="description" v-html="description"></div>
      <b-row>
        <b-col cols="8">
          <b-pagination
            :limit="limitPages"
            :total-rows="totalRows"
            :per-page="perPage"
            v-model="page"
          />
        </b-col>
        <b-col cols="4" class="text-right">
          <p>{{$t('messages.paginate', {total: totalRows})}}</p>
        </b-col>
      </b-row>
    </div>
    <div v-else class="table-toolbar style-2">
      <div class="search-box">
        <div class="flex">
          <b-form-builder
            :inline="true"
            v-if="!_.isEmpty(searchFields)"
            :fields="searchFields"
            :action="searchUri"
            v-model="searchModel"
            :submitText="$t('actions.search')"
            backText
            method="get"
            :on-submit="onSearch"
          >
            <div slot="extra-buttons" class="ml-2">
              <b-button
                type="button"
                @click="searchAndExport"
                variant="success"
                v-if="_.get(actions, 'export')"
              >{{$t('actions.search_and_export')}}</b-button>
              <iframe :src="iframeSrc" style="width:0;height:0;border:none;"></iframe>
            </div>
          </b-form-builder>
          <b-btn
            :to="'/page/' + resourceUri + '.create'"
            variant="link"
            v-if="_.get(actions,'toolbar.create') !== false"
          >
            <i class="iconfont icon-xinjianshiti"></i>
            {{$t('actions.create')}}
          </b-btn>
          <b-btn
            @click="fetchGrid"
            variant="link"
            v-if="_.get(actions, 'toolbar.reload') !== false"
          >
            <i class="iconfont icon-shuaxin"></i>
            {{$t('actions.reload')}}
          </b-btn>
        </div>
        <!-- <b-pagination :limit="limitPages" :total-rows="totalRows" :per-page="perPage" v-model="page" /> -->
        <div class="flex">
          <div class="result">共{{totalRows}}个结果</div>
          <div class="pagination">
            <span class="left-arrow iconfont icon-tuichu" @click="previousPage"></span>
            <div class="go-page flex">
              <input type="number" v-model="inputPage">
              <div>/{{totalRows == 0 ? 1 : Math.ceil(totalRows/limitPages)}}</div>
              <button @click="goPage">GO</button>
            </div>
            <span class="right-arrow iconfont icon-jinru" @click="nextPage"></span>
          </div>
        </div>
      </div>
    </div>
    <b-table
      class="data-table bg-white"
      :sort-by.sync="sortBy"
      :sort-desc.sync="sortDesc"
      :no-local-sorting="true"
      :fields="fields"
      :items="items"
    >
      <template
        v-for="(field, key) in _.omit(fields, '_actions')"
        :slot="`HEAD_${key}`"
      >
        <div
          :key="key"
          :class="{'text-right': ['number'].includes(field.type)}"
        >{{field.label || key}}</div>
      </template>
      <template v-for="(field, key) in fields" :slot="key" slot-scope="row">
        <b-data-value
          :field="field"
          :key="key"
          :lang="currentLanguage"
          :name="key"
          :model="row.item"
          short-id
        />
      </template>
      <template slot="_actions" slot-scope="row">
        <b-btn
          size="sm"
          class="mr-2"
          v-for="(button, key) in _.get(actions, 'addon')"
          :key="key"
          v-bind="button"
        >{{button.label}}</b-btn>
        <b-btn
          size="sm"
          class="mr-2"
          variant="success"
          @click.stop="show(row.item)"
          v-if="_.get(actions, 'buttons.show') !== false"
        >
          <i class="icon-eye"></i>
          {{$t('actions.view')}}
        </b-btn>
        <b-btn
          size="sm"
          class="mr-2"
          variant="primary"
          @click.stop="edit(row.item)"
          v-if="_.get(actions, 'buttons.edit') !== false"
        >
          <i class="icon-pencil"></i>
          {{$t('actions.edit')}}
        </b-btn>
        <b-btn
          size="sm"
          class="mr-2"
          variant="second"
          @click.stop="remove(row.item)"
          v-if="_.get(actions, 'buttons.delete') !== false"
        >
          <i class="icon-trash"></i>
          {{$t('actions.delete')}}
        </b-btn>
      </template>
    </b-table>
    <div v-if="site.grid_style === 1">
      <b-row>
        <b-col cols="8">
          <b-pagination
            :limit="limitPages"
            :total-rows="totalRows"
            :per-page="perPage"
            v-model="page"
          />
        </b-col>
        <b-col cols="4" class="text-right">
          <p>{{$t('messages.paginate', {total: totalRows})}}</p>
        </b-col>
      </b-row>
    </div>
    <div v-else>
      <div class="footer-pagination">
        <div class="flex">
          <div class="result">共{{totalRows}}个结果</div>
          <div class="pagination">
            <span class="left-arrow iconfont icon-tuichu" @click="previousPage"></span>
            <div class="go-page flex">
              <input type="number" v-model="inputPage">
              <div>/{{totalRows == 0 ? 1 : Math.ceil(totalRows/limitPages)}}</div>
              <button @click="goPage">GO</button>
            </div>
            <span class="right-arrow iconfont icon-jinru" @click="nextPage"></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import BFormBuilder from "./FormBuilder";
import BDataValue from "./DataValue";
import { mapState, mapGetters } from "vuex";
export default {
  components: {
    BFormBuilder,
    BDataValue
  },
  props: {
    resource: {
      type: String,
      required: true
    },
    gridPath: {
      type: String,
      default: "grid",
      required: false
    }
  },
  data() {
    return {
      iframeSrc: null,
      pause: true, //修复切换页面时page等参数的自动变更会导致多次fetch的问题
      page: 1,
      inputPage: 1,
      perPage: 6,
      sortBy: this.$config.primaryKey,
      sortDesc: true,
      description: "",
      fields: {},
      filter: {},
      choices: {},
      totalRows: 0,
      items: [],
      searchFields: {},
      searchModel: {},
      where: {},
      title: "",
      limitPages: 10
    };
  },
  computed: {
    ...mapState(["site", "i18n"]),
    ...mapGetters(["currentMenu", "currentLanguage"]),
    actions() {
      return _.get(this.fields, "_actions");
    },
    header() {
      return `
        ${this.currentMenu.name || ""}
        <small> ${this.resource.toUpperCase()} </small>
      `;
    },
    with() {
      return _.filter(
        _.map(
          this.fields,
          (v, k) =>
            v.ref &&
            v.ref
              .split(".")
              .slice(0, -1)
              .join(".")
        )
        //.concat(_.map(this.fields, (v, k) => (v.ref ? k : null)))
      );
    },
    searchUri() {
      return this.resource;
    },
    resourceUri() {
      return [this.site.resource_prefix, this.resource]
        .map(v => v.trim("/"))
        .filter(v => v)
        .join("/");
    },
    gridUri() {
      return [this.site.resource_prefix, this.resource, this.gridPath]
        .filter(v => v)
        .join("/");
    },
    sort: {
      get() {
        if (!this.sortBy) {
          return null;
        }
        return {
          [this.sortBy]: this.sortDesc ? -1 : 1
        };
      },
      set(val) {
        for (let k in val) {
          this.sortBy = k;
          this.sortDesc = val === -1;
        }
      }
    },
    query: {
      get() {
        return {
          sort: this.sort,
          page: this.page,
          perPage: this.perPage,
          with: this.with,
          where: this.where
        };
      },
      set(val) {
        this.sort = val.sort;
        this.page = val.page;
        this.perPage = val.perPage;
        this.where = val.where;
      }
    }
  },
  watch: {
    "site.fetched"(val) {
      if (val) {
        this.fetchGrid(true);
      }
    },
    "$route.params.resource"() {
      this.inputPage = 1;
      this.pause = true;
      this.fetchGrid(true);
    },
    page: "fetch",
    sort: "fetch",
    where: "fetch",
    "$route.query.query"() {
      this.applyQuery();
      this.fetch();
    }
    // query(val) {
    //   this.$emit("change query", val);
    //   // this.$router.push({
    //   //   query: {
    //   //     query: JSON.stringify(val)
    //   //   }
    //   // });
    // }
  },
  methods: {
    goPage() {
      const totalPages = Math.ceil(this.totalRows / this.limitPages);
      if (this.inputPage <= 0 || this.inputPage > totalPages) {
        this.$snotify.warning("请输入正确页码");
        this.inputPage = 1;
        this.page = 1;
        return;
      }
      this.page = this.inputPage;
    },
    previousPage() {
      // const totalPages = Math.ceil(this.totalRows/this.limitPages)
      if (this.inputPage > 1) {
        this.inputPage--;
        this.page = this.inputPage;
      } else {
        this.$snotify.warning("已是第一页");
        this.inputPage = 1;
        this.page = 1;
      }
    },
    nextPage() {
      const totalPages = Math.ceil(this.totalRows / this.limitPages);
      if (this.inputPage < totalPages) {
        this.inputPage++;
        this.page = this.inputPage;
      } else {
        this.$snotify.warning("后面没有了");
        this.inputPage = 1;
        this.page = 1;
      }
    },
    fetch() {
      if (this.pause) {
        return;
      }
      this.pause = true;
      this.$http
        .get(this.resourceUri, {
          params: {
            query: JSON.stringify(this.query)
          }
        })
        .then(({ data }) => {
          const {
            data: items,
            total,
            perPage,
            fields,
            searchFields,
            searchModel
          } = data;
          fields && (this.fields = fields);
          searchFields && (this.searchFields = searchFields);
          searchModel && (this.searchModel = searchModel);
          this.items = items;
          this.description = data.description;
          this.totalRows = total;
          this.perPage = perPage;
          this.pause = false;
        });
    },
    searchAndExport() {
      const query = JSON.stringify({
        where: _.clone(this.searchModel),
        with: _.clone(this.with)
      });
      this.iframeSrc = "";
      setTimeout(() => {
        this.iframeSrc = `${global.API_URI}${
          this.resourceUri
        }/export?query=${query}&token=${this.$store.state.auth.token}`;
      }, 50);
    },
    fetchGrid(fetchData = false) {
      // if (this.$store.state.site.use_field_apis === false) {
      //   this.pause = false;
      //   this.applyQuery();
      //   this.fetch();
      //   return
      // }
      this.query = {};
      this.$http.get(this.gridUri).then(({ data }) => {
        this.fields = data.fields;
        if (!this.fields._actions && this.fields._actions !== false) {
          this.fields._actions = {};
        }
        if (this.fields._actions) {
          if (!this.fields._actions.label) {
            this.fields._actions.label = "";
          }
        }
        this.searchFields = data.searchFields;
        this.searchModel = data.searchModel;
        this.pause = false;
        if (fetchData) {
          this.applyQuery();
          this.fetch();
        }
      });
    },
    applyQuery() {
      const query = this.$route.query.query;
      if (!query) {
        this.query = {};
        return;
      }
      this.query = _.isString(query) ? JSON.parse(query) : query;
      // this.searchModel = this.where
    },
    get(item, path) {
      const [model, field] = path.split(".");
      return item[model][field];
    },
    show(item) {
      this.$router.push({
        path: this.resource + "/" + item[this.$config.primaryKey]
      });
    },
    edit(item) {
      if (this.site.grid_style == 2) {
        return this.$router.push({
          path: `/page/${this.resource}.${item[this.$config.primaryKey]}.edit`
        });
      }
      this.$router.push({
        path: this.resource + "/" + item[this.$config.primaryKey] + "/edit"
      });
    },
    remove(item) {
      if (window.confirm(this.$t("messages.confirm_delete"))) {
        this.$http
          .delete(this.resourceUri + "/" + item[this.$config.primaryKey])
          .then(() => {
            this.$snotify.success(this.$t("messages.deleted"));
            this.fetch();
          });
      }
    },
    removeAll() {
      if (window.confirm(this.$t("messages.confirm_delete_all"))) {
        this.$http.delete(this.resourceUri).then(() => {
          this.$snotify.success(this.$t("messages.deleted_all"));
          this.fetch();
        });
      }
    },

    onSearch() {
      this.where = this.searchModel;
      this.fetch();
    }
  },

  mounted() {
    this.site.fetched && this.fetchGrid(true);

    // console.log('mounted');
  },
  created() {
    // this.applyQuery();
  }
};
</script>
