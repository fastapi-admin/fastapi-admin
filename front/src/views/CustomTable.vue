<template>
  <div class="custom-table">
    <div class="row">
      <div class="col col-md-8 d-none">
        <!-- <legend v-html="table.title || header"></legend> -->
      </div>
      <div class="col col-md-12">
        <b-btn
          class="mr-2"
          :to="uri + '/create'"
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
        >{{button.label}}
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
            >{{$t('actions.search_and_export')}}
            </b-button>
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
          <b-select v-model="perPage" :options="pages" class="mx-2">
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
        selectable
        :per-page="perPage"
        @row-selected="onRowSelected"
        :select-mode="selectModel"
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
          >{{field.label || key}}
          </div>
        </template>

        <template v-slot:cell()="data">
          <template v-if="['datetime', 'date'].includes(data.field.type)">
            {{$d(new Date(data.value), 'long')}}
          </template>
          <template v-else-if="['image'].includes(data.field.type)">
            <b-img width="50px" class="type-image" :src="data.value" fluid/>
          </template>
          <template v-else-if="['link'].includes(data.field.type)">
            <a :class="data.field.classes" :href="data.value" :target="data.field.target">
              <i :class="data.field.icon" v-if="data.field.icon"></i>
              {{data.value}}
            </a>
          </template>
          <template v-else-if="['switch', 'boolean', 'checkbox'].includes(data.field.type)">
            <b-badge :variant="data.value ? 'success' : 'danger'">
              {{data.value ? 'Yes' : 'No'}}
            </b-badge>
          </template>
          <template v-else-if="['html'].includes(data.field.type)">
            <div v-html="data.value" class=" data-value-html"></div>
          </template>
          <template v-else-if="['select', 'select2', 'radiolist', 'checkboxlist'].includes(data.field.type)">
            {{ _.find(data.field.options,{value:data.value}).text }}
          </template>
          <template v-else>
            {{ data.value}}
          </template>
        </template>

        <template v-for="(field, key) in table.fields" :slot="key" slot-scope="row">
          <b-data-value :field="field" :key="key" :name="key" :model="row.item" :pk="pk" short-id/>
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
          >{{field.label}}
          </b-button>
          <b-btn
            v-if="actions.edit !== false"
            variant="success"
            size="sm"
            :to="`${uri}/${row.item[pk]}`"
            class="mr-1"
          >{{$t('actions.view')}}
          </b-btn>
          <b-btn
            v-if="actions.edit !== false"
            variant="primary"
            size="sm"
            :to="`${uri}/${row.item[pk]}/edit`"
            class="mr-1"
          >{{$t('actions.edit')}}
          </b-btn>
          <b-btn
            v-if="actions.delete !== false"
            size="sm"
            @click.stop="remove(row.item[pk])"
          >{{$t('actions.delete')}}
          </b-btn>
        </template>
      </b-table>
      <div class="form-inline my-2">
        <b-button class="mr-1" size="sm" @click="selectAllRows">{{ $t("actions.select_all") }}</b-button>
        <b-button class="mr-1" size="sm" @click="clearSelected">{{ $t("actions.clear_selected")}}</b-button>
        <b-form-select class="mr-1" size="sm" v-model="selectBulkAction" :options="bulkActions"></b-form-select>
        <b-button @click="submitBulk" size="sm" variant="primary">{{ $t("actions.submit")}}</b-button>
      </div>
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
  import {mapState, mapGetters} from "vuex";
  import types from "../store/types";
  import _ from "lodash";
  import {saveAs} from 'file-saver';

  export default {
    components: {},
    props: {},
    data() {
      return {
        init: false,
        loaded: false,
        table: {},
        modes: ['multi', 'single', 'range'],
        selectModel: 'range',
        total: 0,
        pageLimit: 10,
        currentPage: 1,
        sortBy: this.pk,
        sortDesc: true,
        sortDirection: null,
        perPage: 10,
        where: {},
        pk: null,
        selected_pk_list: [],
        bulkActions: {},
        selectBulkAction: null,
        pages: [10, 50, 100]
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
      columns() {
        return Object.entries(this.table.fields).map(([name, field]) => {
          return {
            key: name,
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
        return this.site.resource_prefix + '/' + this.resource.replace(/\./g, "/");
      }
    },
    methods: {
      submitBulk() {
        if (window.confirm(this.$t("messages.confirm_bulk_action"))) {
          this.$http.post(this.uri + '/bulk/' + this.selectBulkAction, {
            pk_list: this.selected_pk_list
          }).then(() => {
            this.$snotify.success(this.$t("messages.bulk_success"));
            this.fetch();
          });
        }
      },
      selectAllRows() {
        this.$refs.table.selectAllRows()
      },
      onRowSelected(items) {
        this.selected_pk_list = _.map(items, item => {
          return item[this.pk];
        })
      },
      clearSelected() {
        this.$refs.table.clearSelected()
      },
      doSearch(params) {
        this.where = _.omitBy(params, v => v === null);
        this.$refs.table.refresh();
      },
      searchAndExport() {
        const query = JSON.stringify({
          where: _.clone(this.table.searchModel),
          with: _.clone(this.populate)
        });
        this.$http.get(this.uri + "/export", {
          responseType: 'arraybuffer',
          params: {
            query: query
          }
        }).then(res => {
          const blob = new Blob([res.data]);
          saveAs(blob, `${this.resource}.xlsx`)
        })
      },
      applyRouteQuery() {
        const {sort = {}, page = 1, where = {}} = JSON.parse(
          this.$route.query.query || "{}"
        );
        const [sortBy, sortDesc] = Object.entries(sort).pop() || [];
        sortBy && (this.sortBy = sortBy);

        if (sortDesc) {
          this.sortDesc = sortDesc === -1;
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
          size: ctx.perPage,
          sort: {[ctx.sortBy]: this.sortDesc ? -1 : 1},
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
            const {total, data} = res.data;
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
          _.mapValues(res.data.bulk_actions, action => {
            action.text = this.$t(`actions.${action.text}`)
          });

          this.bulkActions = res.data.bulk_actions;

          _.mapValues(res.data.fields, field => {
            field.thClass = "bg-light";
          });

          this.table = res.data;
          this.pk = res.data.pk;

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
        }).catch(error => {
          this.table = {}
        });
      },
    },
    mounted() {
    },
    created() {
      this.applyRouteQuery();

      this.fetch();
      // this.fetchTable();
    }
  };
</script>
