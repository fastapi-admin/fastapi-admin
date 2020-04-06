<template>
  <div>
    <b-row>
      <b-col class="h-scroll" :cols="6" md="3" lg="2" xl="2" 
      :class="{[`fold-${foldLevel}`]: true}">
        <b-sidebar :collapsed="collapsed"></b-sidebar>
      </b-col>
      <b-col class="h-scroll" style="overflow-x: auto;">
        <main class="pt-3">
          <b-loading
            :active="$store.state.loading && $store.state.site.enable_loading"
            spinner="bar-fade-scale"
            style="height:100vh;"
          />
          <ol class="breadcrumb" v-if="false">
            <li class="breadcrumb-item" :key="index" v-for="(item, index) in path">
              <span class="active" v-if="isLast(index)">{{ item }}</span>
              <router-link :to="item" v-else>{{ item }}</router-link>
            </li>
          </ol>
          <div class>
            <custom-component :config="$store.state.site.header"></custom-component>
            <div class="px-2">
              <div class="page-header h2">
                <b-btn variant="light" class="mr-2" @click="toggleSidebar">
                  <i class="icon-menu"></i>
                </b-btn>
                <span v-if="$store.state.site.page_header" v-html="$store.state.site.page_header"></span>
              </div>
              <div class="page-body">
                <router-view class="animated fadeIn"/>
              </div>
            </div>
          </div>
          <b-footer v-if="$store.state.site.footer"/>
        </main>
      </b-col>
    </b-row>

    <!-- <b-file-manager></b-file-manager> -->
  </div>
</template>

<script>
import BHeader from "../components/Header";
import BSidebar from "../components/Sidebar";
import BFooter from "../components/Footer";
import { mapState } from "vuex";
// import BFileManager from "../components/FileManager";

export default {
  components: {
    BSidebar,
    BFooter
    // BFileManager
  },
  computed: {
    ...mapState(["site"]),
    collapsed() {
      return this.foldLevel > 0;
    }
  },
  data() {
    return {
      path: [],
      header: "",
      foldLevel: 0
    };
  },
  watch: {},
  methods: {
    toggleSidebar() {
      if (++this.foldLevel > 2) {
        this.foldLevel = 0;
      }
    }
  },
  created() {}
};
</script>

<style>
.left-side {
  overflow: hidden;
}
.fold-0{
  max-width:16em;
}
.fold-1 {
  flex: 0 0 8em !important;
  text-align: center;
}
.fold-2 {
  flex: 0 0 0 !important;
  overflow:hidden;
  height: 0;
  padding:0;
}
.h-scroll {
  transition: all 0.2s;
  height: 100vh;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}
/* main.main {
  margin-left: 200px;
  padding-bottom: 2em;
} */
</style>
