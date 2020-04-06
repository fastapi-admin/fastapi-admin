<template>
  <header class="app-header navbar">
    <button display="md" mobile="true" type="button" class="d-lg-none navbar-toggler">
      <span class="navbar-toggler-icon"></span>
    </button>
    <a href="#/dashboard#" class="navbar-brand" target="_self">
      <img
        src="img/brand/logo.svg"
        width="89"
        height="25"
        alt="CoreUI Logo"
        class="navbar-brand-full"
      >
      <img
        src="img/brand/sygnet.svg"
        width="30"
        height="30"
        alt="CoreUI Logo"
        class="navbar-brand-minimized"
      >
    </a>
    <button display="lg" type="button" class="d-md-down-none navbar-toggler">
      <span class="navbar-toggler-icon"></span>
    </button>
    <ul class="navbar-nav d-md-down-none">
      <li class="nav-item px-3">
        <a href="#/dashboard" class="nav-link active" target="_self">Dashboard</a>
      </li>
      <li class="nav-item px-3">
        <a href="#/users" class="nav-link" target="_self">Users</a>
      </li>
      <li class="nav-item px-3">
        <a href="#" target="_self" class="nav-link">Settings</a>
      </li>
    </ul>
    <ul class="navbar-nav ml-auto">
      <li class="nav-item d-md-down-none">
        <a href="#" target="_self" class="nav-link">
          <li id="__BVID__11" class="nav-item b-nav-dropdown dropdown">
            <a
              href="#"
              id="__BVID__11__BV_button_"
              aria-haspopup="true"
              aria-expanded="false"
              class="nav-link"
            >
              <i class="icon-bell"></i>
              <span class="badge badge-danger badge-pill">5</span>
            </a>
            <div aria-labelledby="__BVID__11__BV_button_" class="dropdown-menu dropdown-menu-right">
              <div class="dropdown-header dropdown-menu-lg text-center">
                <strong>You have 5 notifications</strong>
              </div>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <i class="icon-user-follow text-success"></i> New user registered
              </a>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <i class="icon-user-unfollow text-danger"></i> User deleted
              </a>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <i class="icon-chart text-info"></i> Sales report is ready
              </a>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <i class="icon-basket-loaded text-primary"></i> New client
              </a>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <i class="icon-speedometer text-warning"></i> Server overloaded
              </a>
              <div class="dropdown-header text-center">
                <strong>Server</strong>
              </div>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <div class="text-uppercase mb-1">
                  <small>
                    <b>CPU Usage</b>
                  </small>
                </div>
                <div class="progress-xs progress">
                  <div
                    role="progressbar"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    aria-valuenow="25"
                    class="progress-bar bg-info"
                    style="width: 25%;"
                  >
                    <!---->
                  </div>
                </div>
                <small class="text-muted">348 Processes. 1/4 Cores.</small>
              </a>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <div class="text-uppercase mb-1">
                  <small>
                    <b>Memory Usage</b>
                  </small>
                </div>
                <div class="progress-xs progress">
                  <div
                    role="progressbar"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    aria-valuenow="70"
                    class="progress-bar bg-warning"
                    style="width: 70%;"
                  >
                    <!---->
                  </div>
                </div>
                <small class="text-muted">11444GB/16384MB</small>
              </a>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <div class="text-uppercase mb-1">
                  <small>
                    <b>SSD 1 Usage</b>
                  </small>
                </div>
                <div class="progress-xs progress">
                  <div
                    role="progressbar"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    aria-valuenow="90"
                    class="progress-bar bg-danger"
                    style="width: 90%;"
                  >
                    <!---->
                  </div>
                </div>
                <small class="text-muted">243GB/256GB</small>
              </a>
            </div>
          </li>
        </a>
      </li>
      <li class="nav-item d-md-down-none">
        <a href="#" target="_self" class="nav-link">
          <li id="__BVID__20" class="nav-item b-nav-dropdown dropdown">
            <a
              href="#"
              id="__BVID__20__BV_button_"
              aria-haspopup="true"
              aria-expanded="false"
              class="nav-link"
            >
              <i class="icon-list"></i>
              <span class="badge badge-warning badge-pill">15</span>
            </a>
            <div aria-labelledby="__BVID__20__BV_button_" class="dropdown-menu dropdown-menu-right">
              <div class="dropdown-header dropdown-menu-lg text-center">
                <strong>You have 15 pending tasks</strong>
              </div>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <div class="small mb-1">Upgrade NPM &amp; Bower
                  <span class="float-right">
                    <strong>0%</strong>
                  </span>
                </div>
                <div class="progress-xs progress">
                  <div
                    role="progressbar"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    aria-valuenow="0"
                    class="progress-bar bg-info"
                    style="width: 0%;"
                  >
                    <!---->
                  </div>
                </div>
              </a>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <div class="small mb-1">ReactJS Version
                  <span class="float-right">
                    <strong>25%</strong>
                  </span>
                </div>
                <div class="progress-xs progress">
                  <div
                    role="progressbar"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    aria-valuenow="25"
                    class="progress-bar bg-danger"
                    style="width: 25%;"
                  >
                    <!---->
                  </div>
                </div>
              </a>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <div class="small mb-1">VueJS Version
                  <span class="float-right">
                    <strong>50%</strong>
                  </span>
                </div>
                <div class="progress-xs progress">
                  <div
                    role="progressbar"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    aria-valuenow="50"
                    class="progress-bar bg-warning"
                    style="width: 50%;"
                  >
                    <!---->
                  </div>
                </div>
              </a>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <div class="small mb-1">Add new layouts
                  <span class="float-right">
                    <strong>75%</strong>
                  </span>
                </div>
                <div class="progress-xs progress">
                  <div
                    role="progressbar"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    aria-valuenow="75"
                    class="progress-bar bg-info"
                    style="width: 75%;"
                  >
                    <!---->
                  </div>
                </div>
              </a>
              <a role="menuitem" href="#" target="_self" class="dropdown-item">
                <div class="small mb-1">Angular 2 Cli Version
                  <span class="float-right">
                    <strong>100%</strong>
                  </span>
                </div>
                <div class="progress-xs progress">
                  <div
                    role="progressbar"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    aria-valuenow="100"
                    class="progress-bar bg-success"
                    style="width: 100%;"
                  >
                    <!---->
                  </div>
                </div>
              </a>
              <a role="menuitem" href="#" target="_self" class="dropdown-item text-center">
                <strong>View all tasks</strong>
              </a>
            </div>
          </li>
        </a>
      </li>
      <li class="nav-item d-md-down-none">
        <a href="#" target="_self" class="nav-link">
          <li id="__BVID__33" class="nav-item b-nav-dropdown dropdown">
            <a
              href="#"
              id="__BVID__33__BV_button_"
              aria-haspopup="true"
              aria-expanded="false"
              class="nav-link"
            >
              <i class="icon-envelope-letter"></i>
              <span class="badge badge-info badge-pill">7</span>
            </a>
            <div aria-labelledby="__BVID__33__BV_button_" class="dropdown-menu dropdown-menu-right">
              <div class="dropdown-menu-lg">
                <div class="dropdown-header text-center">
                  <strong>You have 7 messages</strong>
                </div>
                <a role="menuitem" href="#" target="_self" class="dropdown-item">
                  <div class="message">
                    <div class="pt-3 mr-3 float-left">
                      <div class="avatar">
                        <img
                          src="img/avatars/7.jpg"
                          alt="admin@bootstrapmaster.com"
                          class="img-avatar"
                        >
                        <span class="avatar-status bg-success"></span>
                      </div>
                    </div>
                    <div>
                      <small class="text-muted">John Doe</small>
                      <small class="text-muted float-right mt-1">Just now</small>
                    </div>
                    <div class="text-truncate font-weight-bold">
                      <span class="fa fa-exclamation text-danger"></span> Important message
                    </div>
                    <div
                      class="small text-muted text-truncate"
                    >Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt...</div>
                  </div>
                </a>
                <a role="menuitem" href="#" target="_self" class="dropdown-item">
                  <div class="message">
                    <div class="pt-3 mr-3 float-left">
                      <div class="avatar">
                        <img
                          src="img/avatars/6.jpg"
                          alt="admin@bootstrapmaster.com"
                          class="img-avatar"
                        >
                        <span class="avatar-status bg-warning"></span>
                      </div>
                    </div>
                    <div>
                      <small class="text-muted">Jane Doe</small>
                      <small class="text-muted float-right mt-1">5 minutes ago</small>
                    </div>
                    <div class="text-truncate font-weight-bold">Lorem ipsum dolor sit amet</div>
                    <div
                      class="small text-muted text-truncate"
                    >Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt...</div>
                  </div>
                </a>
                <a role="menuitem" href="#" target="_self" class="dropdown-item">
                  <div class="message">
                    <div class="pt-3 mr-3 float-left">
                      <div class="avatar">
                        <img
                          src="img/avatars/5.jpg"
                          alt="admin@bootstrapmaster.com"
                          class="img-avatar"
                        >
                        <span class="avatar-status bg-danger"></span>
                      </div>
                    </div>
                    <div>
                      <small class="text-muted">Janet Doe</small>
                      <small class="text-muted float-right mt-1">1:52 PM</small>
                    </div>
                    <div class="text-truncate font-weight-bold">Lorem ipsum dolor sit amet</div>
                    <div
                      class="small text-muted text-truncate"
                    >Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt...</div>
                  </div>
                </a>
                <a role="menuitem" href="#" target="_self" class="dropdown-item">
                  <div class="message">
                    <div class="pt-3 mr-3 float-left">
                      <div class="avatar">
                        <img
                          src="img/avatars/4.jpg"
                          alt="admin@bootstrapmaster.com"
                          class="img-avatar"
                        >
                        <span class="avatar-status bg-info"></span>
                      </div>
                    </div>
                    <div>
                      <small class="text-muted">Joe Doe</small>
                      <small class="text-muted float-right mt-1">4:03 AM</small>
                    </div>
                    <div class="text-truncate font-weight-bold">Lorem ipsum dolor sit amet</div>
                    <div
                      class="small text-muted text-truncate"
                    >Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt...</div>
                  </div>
                </a>
                <a role="menuitem" href="#" target="_self" class="dropdown-item text-center">
                  <strong>View all messages</strong>
                </a>
              </div>
            </div>
          </li>
        </a>
      </li>
      <li class="nav-item d-md-down-none">
        <a href="#" target="_self" class="nav-link">
          <li id="__BVID__36" class="nav-item b-nav-dropdown dropdown">
            <a
              href="#"
              id="__BVID__36__BV_button_"
              aria-haspopup="true"
              aria-expanded="false"
              class="nav-link"
            >
              <i class="icon-location-pin"></i>
            </a>
            <div aria-labelledby="__BVID__36__BV_button_" class="dropdown-menu dropdown-menu-right">
              <div>
                <h6 class="text-capitalize text-center">your dropdown</h6>
                <ol>
                  <li>one</li>
                  <li>two</li>
                  <li>three</li>
                </ol>
              </div>
            </div>
          </li>
        </a>
      </li>
      <li id="__BVID__39" class="nav-item b-nav-dropdown dropdown">
        <a
          href="#"
          id="__BVID__39__BV_button_"
          aria-haspopup="true"
          aria-expanded="false"
          class="nav-link"
        >
          <img src="img/avatars/6.jpg" alt="admin@bootstrapmaster.com" class="img-avatar">
        </a>
        <div aria-labelledby="__BVID__39__BV_button_" class="dropdown-menu dropdown-menu-right">
          <div class="dropdown-header text-center">
            <strong>Account</strong>
          </div>
          <a role="menuitem" href="#" target="_self" class="dropdown-item">
            <i class="fa fa-bell-o"></i> Updates
            <span class="badge badge-info">42</span>
          </a>
          <a role="menuitem" href="#" target="_self" class="dropdown-item">
            <i class="fa fa-envelope-o"></i> Messages
            <span class="badge badge-success">42</span>
          </a>
          <a role="menuitem" href="#" target="_self" class="dropdown-item">
            <i class="fa fa-tasks"></i> Tasks
            <span class="badge badge-danger">42</span>
          </a>
          <a role="menuitem" href="#" target="_self" class="dropdown-item">
            <i class="fa fa-comments"></i> Comments
            <span class="badge badge-warning">42</span>
          </a>
          <div class="dropdown-header text-center">
            <strong>Settings</strong>
          </div>
          <a role="menuitem" href="#" target="_self" class="dropdown-item">
            <i class="fa fa-user"></i> Profile
          </a>
          <a role="menuitem" href="#" target="_self" class="dropdown-item">
            <i class="fa fa-wrench"></i> Settings
          </a>
          <a role="menuitem" href="#" target="_self" class="dropdown-item">
            <i class="fa fa-usd"></i> Payments
            <span class="badge badge-secondary">42</span>
          </a>
          <a role="menuitem" href="#" target="_self" class="dropdown-item">
            <i class="fa fa-file"></i> Projects
            <span class="badge badge-primary">42</span>
          </a>
          <div role="separator" class="dropdown-divider"></div>
          <a role="menuitem" href="#" target="_self" class="dropdown-item">
            <i class="fa fa-shield"></i> Lock Account
          </a>
          <a role="menuitem" href="#" target="_self" class="dropdown-item">
            <i class="fa fa-lock"></i> Logout
          </a>
        </div>
      </li>
    </ul>
    <button display type="button" class="d-none d-lg-block navbar-toggler">
      <span class="navbar-toggler-icon"></span>
    </button>
  </header>
</template>
