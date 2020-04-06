const _ = require("lodash");
// also you can use other locales
const faker = require("faker/locale/en");
const inflection = require("inflection");
String.prototype.slugify = function() {
  return inflection.dasherize(this.toLowerCase());
};
const config = require("./config");

// Categories
const categories = {
  data: [],
  fields: {
    [config.primaryKey]: { label: "ID" },
    parent_id: {
      label: "Parent",
      ref: "parent.name",
      type: "tree",
      options: [],
      cols: 4
    },
    slug: { cols: 4, searchable: true },
    name: { cols: 4 },
    created_at: { label: "Created At", type: "datetime", sortable: true },
    _actions: {
      preview: {
        label: "Custom Preview",
        // use lodash.template with { item: `current row data` }
        to: "/rest/categories/<%= item._id %>",
        variant: "warning"
      },
      edit: true,
      delete: true
    }
  }
};

_.times(15, i => {
  const name = inflection.titleize(faker.commerce.department());
  categories.data.push({
    [config.primaryKey]: `c${genId(i)}`,
    parent_id: null,
    slug: name.slugify(),
    name: name,
    created_at: faker.date.recent()
  });
});

categories.data = categories.data.map((v, i) => {
  if (i < 3) {
    return v;
  }
  const parent = _.sample(categories.data);
  if (!parent || parent[config.primaryKey] == v[config.primaryKey]) {
    // return v
  }
  v.parent_id = parent[config.primaryKey];
  v.parent = _.clone(parent);
  return v;
});

function findChildren(
  data = [],
  id = null,
  primaryKey = config.primaryKey,
  foreignKey = "parent_id",
  labelKey = "name"
) {
  const ret = _.filter(data, v => v[foreignKey] == id).map(v => {
    const children = findChildren(data, v[primaryKey]);
    if (!_.isEmpty(children)) {
      v.children = _.clone(children);
    }
    v.value = v[primaryKey];
    v.text = v[labelKey];
    return v;
  });
  return ret;
}

categories.fields.parent_id.options = findChildren(categories.data);

// Users
const users = {
  data: [],
  fields: {
    [config.primaryKey]: { label: "ID" },
    username: { label: "Username", cols: 4, searchable: true },
    password: { listable: false, cols: 4 },
    mobile: { listable: false, cols: 4 },
    avatar: { type: "image", cols: 6 },
    intro: { type: "textarea", cols: 6, listable: false },
    created_at: { label: "Created At", type: "datetime" }
  }
};

_.times(128, i =>
  users.data.push({
    [config.primaryKey]: `a${genId(i)}`,
    username: faker.name.lastName(),
    password: "admin",
    mobile: faker.phone.phoneNumber(),
    avatar: faker.image.image(120, 120),
    intro: faker.lorem.sentences(),
    created_at: faker.date.recent()
  })
);

// Products
const products = {
  data: [],
  fields: {
    [config.primaryKey]: {},

    category_ids: {
      cols: 3,
      label: "Categories",
      multiple: true,
      ref: "categories.name",
      type: "tree",
      options: findChildren(categories.data),
      sortable: true
    },
    // slug: { cols: 3, searchable: true },
    name: {
      cols: 6,
      searchable: true,
      description: "Give me an awesome title."
    },
    views: { type: "number", cols: 3, listable: false },
    sort: { type: "number", cols: 3, sortable: true },
    is_reviewed: { type: "switch", cols: 3 },
    type: {
      type: "radiolist",
      cols: 3,
      options: [
        { text: "Article", value: "article" },
        { text: "Page", value: "page" }
      ],
      searchable: true,
      description: "Which type do you like?"
    },

    image: {
      type: "image",
      cols: 6,
      limit: { width: 320, height: 180, limit: 300 * 1000 }
    },
    body: { type: "html", listable: false, cols: 6 },

    created_at: { label: "Created At", type: "datetime" }
  }
};

_.times(78, i => {
  const cats = _.sampleSize(categories.data, parseInt(Math.random() * 3));
  const name = faker.commerce.productName();
  products.data.push({
    [config.primaryKey]: `b${genId(i)}`,
    category_ids: cats.map(v => v[config.primaryKey]),
    categories: cats,
    name: name,
    slug: name.slugify(),
    // image: faker.image.imageUrl(),
    image: faker.image.image(320, 180),
    body: faker.lorem.paragraphs(),
    is_reviewed: Math.random() > 0.2,
    views: parseInt(Math.random() * 1000),
    sort: parseInt(Math.random() * 200),
    type: _.sample(products.fields.type.options).value,
    created_at: faker.date.recent()
  });
});

function genId(salt) {
  return Number(new Date(2020, 1, 1).getTime() + salt).toString(16);
}

function buildOptions(
  data = [],
  valueField = config.primaryKey,
  titleField = "title"
) {
  // { text: 'Please choose...' }
  return data.map(v => {
    return { text: v[titleField], value: v[valueField] };
  });
}

module.exports = { users, products, categories, genId };
