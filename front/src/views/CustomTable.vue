<template>
  <div class="custom-table">
    <div class="row">
      <div class="col col-md-8 d-none">
        <!-- <legend v-html="table.title || header"></legend> -->
      </div>
      <div class="col col-md-12">
        <b-btn
          class="mr-2"
          :to="'/rest/' + uri + '/create'"
          variant="secondary"
          v-if="_.get(actions,'toolbar.create') !== false"
        >
          <i class="icon-plus"></i>
          {{$t('actions.create')}}
        </b-btn>
        <b-btn
          class="mr-2"
          @click="fetch"
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
    </div>
    <div class>
      <div class="my-2">
        <b-form-builder
          :onSubmit="doSearch"
          back-text
          inline
          v-if="_.keys(table.searchFields).length > 0"
          :submit-text="$t('actions.search')"
          :fields="table.searchFields"
          v-model="table.searchModel"
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
      <div class="row align-items-center">
        <div class="col-md-8">
          <b-pagination
            :limit="pageLimit"
            v-model="currentPage"
            :total-rows="total"
            :per-page="perPage"
          ></b-pagination>
        </div>
        <div class="col-md-4 form-inline justify-content-end">
          <b-select v-model="currentPage" class="mx-2">
            <option v-for="n in Math.ceil(total/perPage)" :key="n" :value="n">{{n}}</option>
          </b-select>

          <span>{{$t('messages.paginate', {total: total})}}</span>
        </div>
      </div>
      <b-table
        class="data-table"
        v-if="table.fields"
        ref="table"
        :items="fetchItems"
        :fields="columns"
        :current-page="currentPage"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :sort-direction="sortDirection"
      >
        <template v-for="(field, key) in table.fields" :slot="`HEAD_${key}`">
          <div
            :key="key"
            class="table-header"
            :class="{'text-right': ['number'].includes(field.type)}"
          >{{field.label || key}}</div>
        </template>
        <template v-for="(field, key) in table.fields" :slot="key" slot-scope="row">
          <b-data-value :field="field" :key="key" :name="key" :model="row.item" short-id/>
        </template>

        <template v-slot:cell(_actions)="row">
          <b-button
            v-for="(field, key) in actions"
            :key="key"
            :to="_.template(field.to)(row)"
            class="mr-1"
            size="sm"
            v-bind="field"
            v-show="field.label"
          >{{field.label}}</b-button>
          <b-btn
            v-if="actions.edit !== false"
            variant="success"
            size="sm"
            :to="`/rest/${uri}/${row.item[$config.primaryKey]}`"
            class="mr-1"
          >{{$t('actions.view')}}</b-btn>
          <b-btn
            v-if="actions.edit !== false"
            variant="primary"
            size="sm"
            :to="`/rest/${uri}/${row.item[$config.primaryKey]}/edit`"
            class="mr-1"
          >{{$t('actions.edit')}}</b-btn>
          <b-btn
            v-if="actions.delete !== false"
            size="sm"
            @click.stop="remove(row.item[$config.primaryKey])"
          >{{$t('actions.delete')}}</b-btn>
        </template>
      </b-table>

      <div class="row align-items-center">
        <div class="col-md-10">
          <b-pagination
            :limit="pageLimit"
            v-model="currentPage"
            :total-rows="total"
            :per-page="perPage"
          ></b-pagination>
        </div>
        <div class="col-md-2 text-right">{{$t('messages.paginate', {total: total})}}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from "vuex";
import types from "../store/types";
import _ from "lodash";

export default {
  components: {},
  props: {},
  data() {
    return {
      init: false,
      loaded: false,
      table: {},
      total: 0, //total rows
      pageLimit: 10, //display how many page buttons
      currentPage: 1,
      sortBy: this.$config.primaryKey,
      sortDesc: true,
      sortDirection: null,
      perPage: 10,
      where: {},
      iframeSrc: ""
    };
  },
  watch: {
    "$route.query"(val) {
      this.applyRouteQuery();
    },
    "$route.params"(val) {
      this.applyRouteQuery();
      this.fetch();
    }
    // page(val) {}
  },
  computed: {
    ...mapState(["site", "i18n", "auth"]),
    ...mapGetters(["currentLanguage"]),
    columns(){
      return Object.entries(this.table.fields).map(([name, field]) => {
        return {
          key:name,
          ...field,
        }
      })
    },
    populate() {
      return _(this.table.fields || {})
        .map("ref")
        .filter()
        .map(v => v.split(".").shift())
        .uniq()
        .toJSON();
    },
    actions() {
      return _.get(this.table, "fields._actions", {});
    },
    resource() {
      return this.$route.params.resource;
    },
    uri() {
      return this.resource.replace(/\./g, "/");
    }
  },
  methods: {
    doSearch(params) {
      this.where = _.omitBy(params, v => v === null);
      this.$refs.table.refresh();
      // console.log(params);
    },
    searchAndExport() {
      const query = JSON.stringify({
        where: _.clone(this.table.searchModel),
        with: _.clone(this.populate)
      });
      this.iframeSrc = "";
      setTimeout(() => {
        this.iframeSrc = `${global.API_URI}${
          this.uri
        }/export?query=${query}&token=${this.$store.state.auth.token}`;
      }, 50);
    },
    applyRouteQuery() {
      const { sort = {}, page = 1, where = {} } = JSON.parse(
        this.$route.query.query || "{}"
      );
      const [sortBy, sortDesc] = Object.entries(sort).pop() || [];
      sortBy && (this.sortBy = sortBy);

      if (sortDesc) {
        this.sortDesc = sortDesc === -1 ? true : false;
      }
      this.total = page * this.perPage;
      this.currentPage = page;
      this.where = where;
      this.init = true;
    },
    remove(id) {
      if (window.confirm("是否删除?")) {
        this.$http.delete(`${this.uri}/${id}`).then(res => {
          this.$snotify.success("删除成功");
          this.$refs.table.refresh();
        });
      }
    },
    fetchItems(ctx) {
      const query = _.merge({}, _.get(this.table, "query"), {
        page: ctx.currentPage,
        sort: { [ctx.sortBy]: this.sortDesc ? -1 : 1 },
        where: this.where,
        with: this.populate
      });
      // console.log(query)

      if (!this.init) {
        // this.$router.replace({
        //   query: { query: JSON.stringify(query) }
        // });
        return [];
      }
      // this.$router.push({
      //   query: { query: JSON.stringify(query) }
      // });
      return this.$http
        .get(this.uri, {
          params: {
            query: JSON.stringify(query)
          }
        })
        .then(res => {
          const { total, data } = res.data;
          this.total = total;
          return data;
        })
        .catch(e => {
          return [];
        });
    },
    fetch() {
      this.init = false;
      this.$http.get(this.uri + "/grid").then(res => {
        _.mapValues(res.data.fields, field => {
          field.thClass = "bg-light";
        });

        this.table = res.data;

        if (_.get(this.table, "fields._actions") !== false) {
          _.set(
            this.table,
            "fields._actions.label",
            this.$t("actions.actions")
          );
        }
        this.init = true;
        if (this.$refs.table) {
          this.$refs.table.refresh();
        }
      });
    }
  },
  mounted() {},
  created() {
    this.applyRouteQuery();

    this.fetch();
    // this.fetchTable();
  }
};
</script>