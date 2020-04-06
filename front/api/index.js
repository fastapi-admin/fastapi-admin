const express = require("express");
const app = express();
const _ = require("lodash");
const faker = require("faker");

const config = require("./config");

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use("/static", express.static(__dirname + "/static"));
app.get("/", (req, res) => {
  res.send({
    welcome: "Test api for rest-admin is running."
  });
});

const router = express.Router();

app.use((req, res, next) => {
  // cors
  res.header("Access-Control-Allow-Origin", "*");
  res.header(
    "Access-Control-Allow-Headers",
    "Authorization,Content-Type,X-Requested-With"
  );
  res.header("Access-Control-Allow-Methods", "*");
  next();
});

// for basic site config
router.get("/site", (req, res) =>
  res.send({
    name: "DASHBOARD", //site name
    locale: "en-US",
    logo: "http://rest-admin.genyii.com/logo.png",
    locale_switcher: true,
    theme_switcher: true,
    theme: "cosmo",
    url: "https://github.com/wxs77577/rest-admin",
    grid_style: 1,
    footer1: `
  <span class="ml-auto">
    GitHub <a href="https://github.com/wxs77577/rest-admin">https://github.com/wxs77577/rest-admin</a>
  </span>
  <script>
  //Baidu Statistic
  var _hmt = _hmt || [];
  (function() {
    var hm = document.createElement("script");
    hm.src = "https://hm.baidu.com/hm.js?8ec67f6e612d57c8a9f2e21a32ddf4ff";
    var s = document.getElementsByTagName("script")[0]; 
    s.parentNode.insertBefore(hm, s);
  })();
  </script>
  `,
    css: [`${req.protocol}://${req.host}/static/custom.css`],
    menu: [
      //site menu
      {
        name: "Home",
        url: "/home",
        exact: true,
        icon: "icon-home"
      },
      {
        name: "Content",
        title: true
      },
      {
        name: "Categories",
        url: "/rest/categories",
        icon: "icon-list"
      },
      {
        name: "Products",
        url: "/rest/products",
        icon: "icon-list"
      },
      {
        name: "Users",
        url: "/rest/users",
        icon: "icon-user"
      },
      {
        name: "System",
        title: true
      },
      {
        name: "Settings",
        url: "/form/site.settings",
        icon: "icon-settings"
        // a custom form.
      },
      {
        name: "Restore Data",
        url: "/page/restore",
        icon: "icon-settings"
        // a custom page.
      },
      {
        divider: true
      },
      {
        name: "Logout",
        url: "/login",
        icon: "icon-lock"
      },

      {
        name: "Github",
        external: true,
        url: "https://github.com/wxs77577/rest-admin",
        icon: "fa fa-github"
      }
    ]
  })
);

// for home page
router.get("/home", (req, res) =>
  res.send({
    title: "Welcome to REST ADMIN",
    description: `<div>Admin dashboard based on vue 2 and bootstrap 4 </div> 
      <div class="font-weight-bold">Please check the XHR requests of **Network** panel in chrome dev-tool for Server-side APIs.</div>
      `,
    button: {
      icon: "icon-people",
      variant: "primary",
      text: "Users",
      to: "/rest/users"
    },
    statics: [
      {
        bg: "info",
        icon: "icon-speedometer",
        value: 5000 + parseInt(Math.random() * 5000),
        title: "Comments",
        progress: 78
      },
      {
        bg: "success",
        icon: "icon-people",
        value: 10000 + parseInt(Math.random() * 10000),
        title: "Users",
        progress: 60
      },
      {
        bg: "warning",
        icon: "icon-basket-loaded",
        value: 100000 + parseInt(Math.random() * 30000),
        title: "Sales",
        progress: 92
      },
      {
        bg: "primary",
        icon: "icon-camrecorder",
        value: 300 + parseInt(Math.random() * 300),
        title: "Videos",
        progress: 67
      }
    ]
  })
);

router.post("/login", (req, res) => {
  const { username, password } = req.body;
  if (username == "admin" && password == "admin") {
    res.send({
      user: { username, password },
      token: "fake token"
    });
  } else {
    res.status(422).send({
      message: "Username or password is incorrect."
    });
  }
});

router.post("/upload", (req, res) => {
  let url = faker.image.avatar();
  switch (req.body.type) {
    case "image":
      url = faker.image.image(320, 140);
      break;
  }
  res.send({
    url
  });
});

const settingForm = {
  title: "App Settings",
  fields: {
    name: { label: "Site Name", input_cols: 4 },
    logo: { label: "Site Logo", type: "image", input_cols: 4 },
    theme_switcher: true,
    menu: {
      type: "array",
      is_table: true,
      fields: {
        name: {},
        _actions: {}
      }
    }
  },
  value: {
    name: "REST ADMIN",
    menu: []
  }
};

router.get("/site/settings", (req, res) => {
  res.send(settingForm);
});

router.post("/site/settings", ({ body }, res) => {
  settingForm.model = body;
  res.send(settingForm);
});

/**
 * CRUD for Resources
 */

let resources = require("./resources");

const rawResources = Object.assign({}, resources);

router.all("/restore", (req, res) => {
  if (req.body.restore) {
    console.log("restore");
    resources = Object.assign({}, rawResources);
  }
  return res.send({
    data: {
      header: "Restore Data",
      fields: {
        restore: { type: "switch", label: "Restore Data ?" }
      }
    },
    template: `
      <div>
        
        <p>如果测试数据被玩坏了。。。</p>
        <b-form-builder :fields="fields" submitText="Yeah!" action="restore"></b-form-builder>
      </div>
    `
  });
});

const resourceRouter = express.Router({
  mergeParams: true
});

// user list data
resourceRouter.get("/", ({ resource, query }, res) => {
  const queryObject = JSON.parse(query.query || "{}");
  const { page = 1, perPage = 10, sort = {}, where = null } = queryObject;

  let data = resource.data;
  if (sort) {
    data = _.orderBy(
      resource.data,
      Object.keys(sort),
      Object.values(sort).map(v => (v === -1 ? "desc" : "asc"))
    );
  }

  if (where) {
    data = _.filter(data, row => {
      let isMatch = true;
      for (let key in where) {
        const value = row[key];
        const search = where[key];
        if (_.isString(value)) {
          isMatch = isMatch && new RegExp(search, "i").test(value);
        } else {
          isMatch = isMatch && value == search;
        }
      }
      return isMatch;
    });
  }

  res.send({
    total: data.length,
    perPage,
    page,
    data: data.slice((page - 1) * perPage, page * perPage)
  });
});

// data table config for listing users
resourceRouter.get("/grid", (req, res) => {
  const { resource, params } = req;
  res.send({
    title: params.resource.replace(/^(\w)/, m => m.toUpperCase()),
    searchModel: {},
    searchFields: _.pickBy(resource.fields, (v, k) => {
      return v.searchable === true;
    }),
    fields: _.pickBy(resource.fields, (v, k) => {
      return v.listable !== false;
    })
  });
});

// data FORM config for editing an user
resourceRouter.get("/form/:id?", ({ resource }, res) => {
  res.send({
    fields: _.pickBy(resource.fields, (v, k) => {
      return (
        v.editable !== false &&
        ![config.primaryKey, "created_at", "updated_at"].includes(k)
      );
    })
  });
});

// data FORM config for editing an user
resourceRouter.get("/view", ({ resource }, res) => {
  res.send({
    fields: _.pickBy(resource.fields, (v, k) => {
      return (
        v.viewable !== false &&
        ![config.primaryKey, "created_at", "updated_at"].includes(k)
      );
    })
  });
});

// single user data
resourceRouter.get("/:id", ({ resource, params }, res) => {
  const model = resource.data.find(v => v[config.primaryKey] == params.id);
  res.send(model);
});

// update
resourceRouter.put("/:id", ({ resource, params, body }, res) => {
  let i = resource.data.findIndex(v => v[config.primaryKey] == params.id);
  resource.data[i] = _.pick(body, Object.keys(resource.fields));
  res.send(resource.data[i]);
});

// create
resourceRouter.post("/", ({ resource, body }, res) => {
  const data = _.pick(body, Object.keys(resource.fields));
  data[config.primaryKey] = resources.genId("");
  resource.data.push(data);
  res.send(resource.data[resource.data.length - 1]);
});

// delete
resourceRouter.delete("/:id", ({ resource, params }, res) => {
  let i = resource.data.findIndex(v => v[config.primaryKey] == params.id);
  resource.data.splice(i, 1);
  res.send({
    success: true
  });
});
// delete all
resourceRouter.delete("/", ({ resource }, res) => {
  resource.data.splice(0);
  res.send({
    success: true
  });
});

router.use(
  "/:resource",
  (req, res, next) => {
    req.resource = resources[req.params.resource] || {};
    next();
  },
  resourceRouter
);

app.use("/admin/api", router);
const PORT = process.env.PORT || 8088;
app.listen(PORT, () => {
  global.console.log(`Test API is listening at http://localhost:${PORT}`);
});
