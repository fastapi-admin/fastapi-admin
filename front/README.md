# REST-ADMIN [中文文档](./README-zh.md)

> An Powerful Admin Dashboard based on [Boostrap-Vue](https://github.com/bootstrap-vue/bootstrap-vue/).

Demo: http://rest-admin.genyii.com/ `admin admin`

Please support me on https://afdian.net/@johnny if you like it.
如果觉得有用请在爱发电上赞助我：https://afdian.net/@johnny

## Features

- **Bootswatch Themes**
- Powerful **Data Table** with sorting, pagination, searching, display images...
- Powerful **Edit Form Builder** can display/edit any value of text, image, boolean...
- Fully support for Resource-based CRUD option.
- English based fully i18n support.
- **Highly Configurable** site info. Such as: site name, logo, **Menu** and footer...
- Production ready. It has been used in two projects in our company.

## Screenshots

| -                                                                                       | -                                           |
| --------------------------------------------------------------------------------------- | ------------------------------------------- |
| ![](./screenshots/1.png) Login Page                                                     | ![](./screenshots/home.png) Home page       |
| ![](./screenshots/3.png) Data Table for posts                                           | ![](./screenshots/4.png) Data Form for post |
| ![](./screenshots/tfs-qrcode.png) Wechat Group (Search Wechat `johnny77577` to join in) | ![](./screenshots/tfs-logo.png) Free Videos |

## Quick Start

```bash
git clone git@github.com:wxs77577/rest-admin.git
cd rest-admin
code . # open with vscode [optional]
npm i # or cnpm i

# start with local test api server
npm run test-api # start test api server
npm run serve # start rest admin client
```

> The default username and password of test-api is `admin` and `admin`

### Build

```bash
API_URI=http://localhost:5555/admin/api/ npm run build
```

Then just copy `/dist/admin` folder to the anywhere.

> There is a built-in restful api based on `express` for test.

## Fields Definition

> Used in listing tables and editing forms
> Default PRIMARY_KEY field is `_id`, feel free to change it in `/src/config.json`

Example:

```javascript
{
  "_id": { "label": "ID" },
  "title": { "label": "Title" },
  "type": {
    "label": "Type",
    "type": "select",
    "options": [
      { "text": "Vue", "value": "vue" },
      { "text": "React", "value": "react" },
      { "text": "Angular", "value": "angular" }
    ]
  },
  "body": { "type": "html", "group": "Detail" },
  "steps": {
    "type": "array",
    "group": "Steps",
    "fields": {
      "name": { "label": "Name" },
      "date": { "label": "date" }
    }
  },

  "_actions": {
    // define table view, it's optional.
    "buttons": {
      // define buttons as `false` to hide in actions colum
      "delete": false,
      "edit": false
    },
    "toolbar": {
      // define actions in top toolbar table view
      "extra": [
        // add extra buttons
        { "to": "/form?uri=vouchers/generate", "label": "Generate Vouchers" } //properties of `<b-button>`
      ]
    }
  }
}
```

### Field properties

- `label` Title for display
- `cols` column width, total is 12.
- `input_cols` column width of input control.
- `group` title for tabs in create/edit forms
- `type` Field type, accepted values and additional properties for some fields.
  - `select` raw html `<select>` tag from [b-select](https://bootstrap-vue.js.org/docs/components/form-select) of `bootstrap-vue`
    - `options` e.g. `[{ "text": "Label", "value": "1" }]`
  - `select2` [vue-select](https://github.com/sagalbot/vue-select), like `select2` in jQuery
    - `options` e.g. `[{ "text": "Label", "value": "1" }]`
  - `tree` [vue-treeselect](https://vue-treeselect.js.org/)
    - `options` **use `text` and `value` instead `label` and `id`** e.g. `[{ "text": "Label", "value": "1", "children": [ { "text": "Item1", "value": "2" } ] }]`
  - `date` [vue2-datepicker](https://github.com/mengxiong10/vue2-datepicker) supports **date range**
  - `switch` A iOS-liked switch component
  - `html` An WYSIWYG html editor from [vue-html5-editor](https://github.com/PeakTai/vue-html5-editor)
  - `array` Array values
    - `fields` child fields defination
    - `is_table` display as a table ?
  - `radiolist`
    - `options` e.g. `[{ "text": "Label", "value": "1" }]`
  - `checkboxlist`
    - `options` e.g. `[{ "text": "Label", "value": "1" }]`
  - `checkbox`
  - `file` File uploader
    - `limit` define file limit options of **size** in byets, e.g. `{ size: 1000000 }`
  - `image` Image file uploader with preview.
    - `limit` define file limit options of **width** **height** and **size** in byets, e.g. `{ "width": 320, "height": 180, size: 1000000 }`
  - `audio` like `image`
    - `limit` define file limit options of **size** in byets, e.g. `{ size: 1000000 }`
  - `video` like `image`
    - `limit` define file limit options of **size** in byets, e.g. `{ size: 1000000 }`
  - `textarea`
  - `number`
  - `text`
- `required`
- Any other properties accepted in https://bootstrap-vue.js.org/docs/components/form-input, please notice that every kind of field component has it's own properties.

## APIs

> Tips: check `/api/index.js` :p

Example Base Api Url: http://localhost:8088/admin/api

#### GET `/site` (url: http://localhost:8088/admin/api/site)

Get config data of site

- Returns
  ```javascript
  {
    "name": "Site Name",
    "logo": "http://.../logo.png",
    "locale": "en-US", //or zh-CN
    "locale_switcher": false, //hide locale switcher
    "menu": [
      {
        "name": "Home",
        "url": "/",
        "icon": "fa fa-home"
        // for home page
      },
      {
        "name": "Content",
        "title": true
        // display as a delimiter
      },
      {
        "name": "Posts",
        "url": "/rest/posts",
        "icon": "fa fa-list"
        // url format of resource list: /rest/:resourceName
      },
      {
        "name": "Config",
        "url": "/form?uri=site/settings",
        "icon": "fa fa-cogs"
        // a custom form.
      },
      {
        "name": "Logout",
        "url": "/login",
        "icon": "fa fa-lock"
        // for logout
      }
    ]
  }
  ```

#### POST `/login`

For admin user login

- POST DATA
  ```javascript
  {
    "username": "admin",
    "password": "admin"
  }
  ```
- Returns
  ```javascript
  {
    "user": {
      "username": "admin",
      ...
    },
    "token": "1o2u3h4oi2u3h4jkashdflsda"
  }
  ```
  or with validation errors
  > must response `422` http status.
  ```javascript
  {
    "name": "HttpException",
    "message": [{ "field": "password", "message": "Incorrect password." }]
  }
  ```

#### GET `/:resource`

Fetch all records of a resource.
`:resource` means any resource name. e.g. `/users`, `/posts`...

- Returns **IMPORTANT**
  ```javascript
  {
    "total": 80,
    "perPage": 10,
    "page": 1,
    "data": [
      {...},
      {...},
      {...},
    ]
  }
  ```

#### GET `/:resource/grid`

Fetch grid view config of a resource.
`:resource` means any resource name. e.g. `/users/grid`, `/posts/grid`...

- Returns **IMPORTANT**
  ```javascript
  {
    "searchModel": {},
    "searchFields": {
      render a searching form
      ...see Fields Definition...
    },
    "fields": {
      render a table view
      ...see Fields Definition...
    }
  }
  ```

#### GET `/:resource/form`

Fetch editing form config of a resource.
`:resource` means any resource name. e.g. `/users/form`, `/posts/form`...

- Returns **IMPORTANT**
  ```javascript
  {
    "model": {},
    "fields": {
      render a editing form
      ...see Fields Definition...
    }
  }
  ```

#### POST `/:resource`

create a resource

- POST DATA
  ```javascript
  {
    "_id": "12341234",
    "title": "The New Title",
    ...
  }
  ```
- Returns
  ```javascript
  {
    "_id": "12341234",
    "title": "The New Title",
    ...
  }
  ```

#### PUT `/:resource/:id`

update a resource

- POST DATA (Request Payload)
  ```javascript
  {
    "_id": "12341234",
    "title": "The New Title",
    ...
  }
  ```
- Returns
  ```javascript
  {
    "_id": "12341234",
    "title": "The New Title",
    ...
  }
  ```

#### DELETE `/:resource/:id`

delete a resource

- Returns
  ```javascript
  {
    "success": true
  }
  ```

#### DELETE `/:resource`

delete all

- Returns
  ```javascript
  {
    "success": true
  }
  ```

#### Custom Form ?

> To render a custom form, you need to define a `menu` item in `/site` api, or add an `extra` button of toolbar in `/:resource/grid`.

There are two apis for a custom form:

1. Get form definition

- GET `/site/settings`
- Returns
  ```
  {
    "title": "Form Title",
    "fields": {
      ...see Fields Definition...
    }
  }
  ```

2. Handle submission

- POST `/site/settings`
- Returns
  ```javascript
  {
    "success": true,
    "message": "Well done!", //[optional] will show after form submited.
    "redirect": "/" //[optional] auto redirect after form submited, default is back to the last page.
  }
  ```

## i18n

> Check [vu-i18n](https://github.com/kazupon/vue-i18n/) for detailed documentation.

REST-ADMIN gives built-in support for `en-US` and `zh-CN`, you can change translation files in `/src/i18n/*.json`.

## Thanks to

- Vue.js and Bootstrap v4 based [bootstrap-vue](https://github.com/bootstrap-vue/bootstrap-vue)
- Nice UI from [Core UI](https://coreui.io/)
- i18n component from [vue-i18n](https://github.com/kazupon/vue-i18n/)
