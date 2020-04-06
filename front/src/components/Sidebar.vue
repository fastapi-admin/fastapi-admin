<template>
  <div class="pt-3 pl-3">
    <div class="text-center top">
      <a :href="site.url" target="_blank" v-if="site.logo" v-show="!collapsed">
        <b-img class="site-logo" :src="site.logo" fluid/>
      </a>

      <!-- <b-img class="site-logo" :src="require('../assets/img/gengyi-logo.svg')" fluid style="border-radius: 5px;" /> -->
      <!-- <b-img rounded="circle" :src="auth.user.avatar" height="70" blank-color="#777" alt="avatar" class="m-2" /> -->
      <div class="my-3" v-if="site.sidebar_userinfo !== false" v-show="!collapsed">
        <h5 style="letter-spacing:2px">{{site.name}}</h5>
        <template v-if="auth.user">
          <b-badge class="text-uppercase mr-1" v-if="auth.user.badge">{{auth.user.badge}}</b-badge>
          <span>{{auth.user.username}}</span>
        </template>
      </div>
      <div v-else></div>

      <locale-switcher v-show="!collapsed"></locale-switcher>
      <theme-switcher v-show="!collapsed"></theme-switcher>
    </div>
    <div slot="header"></div>
    <b-nav pills class="sidebar-nav" vertical>
      <template v-for="(item, index) in site.menu">
        <b-nav-text v-if="item.title" :key="index">
          <small class="text-muted">
            <b>{{item.name}}</b>
          </small>
        </b-nav-text>
        <b-nav vertical v-else-if="item.children" :key="index">
          <b-nav-item :to="child.url" :key="child.name" v-for="child in item.children">
            <i class="mr-1" :class="child.icon"></i>
            <span>{{child.name}}</span>
            <b-badge v-bind="child.badge" v-if="child.badge">{{child.badge.text}}</b-badge>
          </b-nav-item>
        </b-nav>
        <b-nav-item :active="$route.path === item.url" :to="item.url" v-else :key="index">
          <i :class="{'mr-2': !collapsed, [item.icon]: true}"></i>
          <span v-show="!collapsed">{{item.name}}</span>
          <b-badge v-bind="item.badge" v-if="item.badge">{{item.badge.text}}</b-badge>
        </b-nav-item>
      </template>
      <slot></slot>
    </b-nav>
    <p></p>
  </div>
</template>
<script>
import ThemeSwitcher from "./ThemeSwitcher";
import LocaleSwitcher from "./LocaleSwitcher";

import { mapState } from "vuex";
export default {
  name: "sidebar",
  props: {
    collapsed: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {};
  },

  computed: {
    ...mapState(["auth", "site"]),
    menu() {
      const menu = [];
      const titleIndices = [];
      this.site.menu.forEach((v, k) => {
        v.title && titleIndices.push(parseInt(k));
      });
      for (let i in titleIndices) {
        menu.push({
          name: this.site.menu[titleIndices[i]].name,
          children: this.site.menu.slice(
            titleIndices[i] + 1,
            titleIndices[parseInt(i) + 1]
          )
        });
      }
      return menu;
    }
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
.site-logo {
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
}
.sidebar-nav {
  .nav-item a {
    color: #666;
    padding: 0.7rem 1rem;
  }
}
.sidebar-nav .nav-item:hover {
  background: #f6f6f6;
}
</style>
