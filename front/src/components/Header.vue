<template>
  <header class="app-header navbar">
    <button class="navbar-toggler mobile-sidebar-toggler d-lg-none" type="button" @click="mobileSidebarToggle">
      <span class="navbar-toggler-icon"></span>
    </button>
    <b-link class="navbar-brand" to="/">
      
    </b-link>
    <button class="navbar-toggler sidebar-toggler d-md-down-none" type="button" @click="sidebarToggle">
      <span class="navbar-toggler-icon"></span>
    </button>
    <b-navbar-nav is-nav-bar class="d-md-down-none">
      <b-nav-item class="px-3">Dashboard</b-nav-item>
      <b-nav-item class="px-3">Users</b-nav-item>
      <b-nav-item class="px-3">Settings</b-nav-item>
    </b-navbar-nav>
    <b-navbar-nav is-nav-bar class="ml-auto">
      <b-nav-item class="d-md-down-none">
        <i class="icon-bell"></i>
        <b-badge pill variant="danger">5</b-badge>
      </b-nav-item>
      <b-nav-item class="d-md-down-none">
        <i class="icon-list"></i>
      </b-nav-item>
      <b-nav-item class="d-md-down-none">
        <i class="icon-location-pin"></i>
      </b-nav-item>
      <b-nav-item-dropdown right no-caret>
        <template slot="button-content">
          <img src="static/img/avatars/6.jpg" class="img-avatar" alt="admin@bootstrapmaster.com">
        </template>
        <b-dropdown-header tag="div" class="text-center"><strong>Account</strong></b-dropdown-header>
          <b-dropdown-item><i class="fa fa-bell-o"></i> Updates<b-badge variant="info">{{itemsCount}}</b-badge></b-dropdown-item>
          <b-dropdown-item><i class="fa fa-envelope-o"></i> Messages<b-badge variant="success">{{itemsCount}}</b-badge></b-dropdown-item>
          <b-dropdown-item><i class="fa fa-tasks"></i> Tasks<b-badge variant="danger">{{itemsCount}}</b-badge></b-dropdown-item>
          <b-dropdown-item><i class="fa fa-comments"></i> Comments<b-badge variant="warning">{{itemsCount}}</b-badge></b-dropdown-item>
          <b-dropdown-header tag="div" class="text-center"><strong>Settings</strong></b-dropdown-header>
          <b-dropdown-item><i class="fa fa-user"></i> Profile</b-dropdown-item>
          <b-dropdown-item><i class="fa fa-wrench"></i> Settings</b-dropdown-item>
          <b-dropdown-item><i class="fa fa-usd"></i> Payments<b-badge variant="default">{{itemsCount}}</b-badge></b-dropdown-item>
          <b-dropdown-item><i class="fa fa-file"></i> Projects<b-badge variant="primary">{{itemsCount}}</b-badge></b-dropdown-item>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item><i class="fa fa-shield"></i> Lock Account</b-dropdown-item>
          <b-dropdown-item><i class="fa fa-lock"></i> Logout</b-dropdown-item>
        </b-nav-item-dropdown>
    </b-navbar-nav>
    <button class="navbar-toggler aside-menu-toggler d-md-down-none" type="button" @click="asideToggle">
      <span class="navbar-toggler-icon"></span>
    </button>
  </header>
</template>
<script>
  
  export default {
    name: 'header',
    components: {
      
    },
    data(){
      return {
        itemsCount: 3
      }
    },
    methods: {
      sidebarToggle (e) {
        e.preventDefault()
        document.body.classList.toggle('sidebar-hidden')
      },
      sidebarMinimize (e) {
        e.preventDefault()
        document.body.classList.toggle('sidebar-minimized')
      },
      mobileSidebarToggle (e) {
        e.preventDefault()
        document.body.classList.toggle('sidebar-mobile-show')
      },
      asideToggle (e) {
        e.preventDefault()
        document.body.classList.toggle('aside-menu-hidden')
      }
    }
  }
</script>
