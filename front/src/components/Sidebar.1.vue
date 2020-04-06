<template>
  <b-aside class="sidebar position-fixed">
    <div class="text-center top">
      <a :href="site.url" target="_blank" v-if="site.logo">
        <img class="site-logo img-fluid" :src="site.logo">
      </a>
      <!-- <b-img class="site-logo" :src="require('../assets/img/gengyi-logo.svg')" fluid style="border-radius: 5px;" /> -->
      <!-- <b-img rounded="circle" :src="auth.user.avatar" height="70" blank-color="#777" alt="avatar" class="m-2" /> -->
      <div class="my-3" v-if="site.sidebar_userinfo !== false">
        <h5 style="letter-spacing:2px">{{site.name}}</h5>
        <template v-if="auth.user">
          <b-badge class="text-uppercase mr-1" v-if="auth.user.badge">{{auth.user.badge}}</b-badge>
          <span>{{auth.user.username}}</span>
        </template>
      </div>
      <div v-else></div>

      <!-- <locale-switcher></locale-switcher> -->
      <!-- <theme-switcher></theme-switcher> -->
    </div>
    <el-menu router>
      <template v-for="(item, index) in site.menu" >
        <el-submenu :index="item.url" :key="index" v-if="item.children">
          <template slot="title">
            <i :class="item.icon"></i>
            <span>{{item.name}}</span>
          </template>
        </el-submenu>
        <el-menu-item :index="item.url" :key="index" v-else>
          <i :class="item.icon"></i>
          <span class="">{{item.name}}</span>
        </el-menu-item>
      </template>
    </el-menu>
  </b-aside>
</template>
<script>
import ThemeSwitcher from "./ThemeSwitcher";
import LocaleSwitcher from "./LocaleSwitcher";

import { mapState } from "vuex";
export default {
  name: "sidebar",

  computed: {
    ...mapState(["auth", "site"])
  },
  components: { LocaleSwitcher, ThemeSwitcher },
  methods: {
    toggle(item) {
      this.$set(item, "open", !item.open);
    }
  }
};
</script>

<style lang="scss">
// .sidebar {
//   z-index: 999;
//   box-shadow: 1px 0 20px rgba(0, 0, 0, 0.1);
//   width: 200px;
//   height: 100vh;
//   overflow: auto;
//   letter-spacing: 1px;
//   padding: 1rem;

//   .site-logo {
//     // border-radius: 1rem;
//     // min-height:3em;
//   }

//   .nav-link {
//     color: #666;
//     display: flex;
//     align-items: center;
//     padding: 0.7rem 1rem;
//     // border-radius: 2rem;
//     // font-weight: 400;

//     &:hover,
//     &.active {
//       // color: #333;
//       // background: #eee;
//     }
//     i {
//       margin-right: 1rem;
//     }
//   }
//   .nav-title {
//     font-size: 0.7rem;
//     font-weight: bold;
//     text-transform: uppercase;
//     color: #ced4da;
//     padding: 1rem 1rem 0.5rem 0;
//   }
// }
</style>
