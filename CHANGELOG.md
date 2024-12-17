# CHANGELOG


## v19.0.0 (2024-12-17)

### Features

- Empty commit to trigger a version bump
  ([`5ae11a7`](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/commit/5ae11a70a2b7594f7f0c5b300da28b670fd504f6))


## v18.1.0 (2024-12-17)

### Chores

- **release**: Preparing 18.1.0
  ([`f91f939`](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/commit/f91f939bbd1fa047f47d1851d7e17e6824fa2c5a))

### Features

- Sumac release ([#11](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/pull/11),
  [`45fef46`](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/commit/45fef4673b36a00c901b7176cf7115c0e90eeb1e))


## v18.0.0 (2024-07-15)

### Features

- Support for redwood ([#9](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/pull/9),
  [`2dbce5e`](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/commit/2dbce5ea1e8332245f5fd3913d4f81ba30cc41cc))

* allow MFEs to be hosted on either the LMS or the CMS

Before all the MFEs that were hosted by path were hosted in the LMS domain. For certain MFEs
  (course-authoring) the CMS domain is more appropriate.

* point the MFEs URLs to either the LMS or the CMS

* handle special cases in the $LMS_HOST/account route.

The `/account/password` endpoint is used in the 'forgot password' flow, for that reason we must
  forward those requests to the LMS.

The `/account/settings` is more specific to the multitenant use case. Some sites may be configured
  to use the legacy pages but the current configuration would send every subpath of `/account/` to
  the MFE, we make an exception for the legacy URL.


## v17.0.0 (2024-06-03)

### Features

- Add support to quince ([#8](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/pull/8),
  [`6811d69`](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/commit/6811d69784792cc9a2ac692a8ee81b6d9e0c6588))


## v16.0.0 (2024-01-26)

### Features

- Add a new setting to toggle the npm packages overrides
  ([#4](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/pull/4),
  [`bfb9e4f`](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/commit/bfb9e4f537e97e73c3e48a604b91f8e78b07c8eb))

- Palm support ([#7](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/pull/7),
  [`5b7eb9d`](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/commit/5b7eb9da9110de66cc402839b12f5d790bf1cbb8))


## v1.2.0 (2023-10-24)

### Features

- Allow dynamic configuration of the assets path
  ([#2](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/pull/2),
  [`91228cc`](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/commit/91228cc1ff0fe0b8e7577e9672bda1c3ab148f7b))

This includes an additional executable script that is mounted to the MFE pod and is run at container
  startup time. The script replaces a placeholder string with the MFE_EXTENSIONS_CDN_URL setting.


## v1.1.0 (2023-09-22)

### Features

- Add routing of MFEs via path
  ([#1](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/pull/1),
  [`e0b837d`](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/commit/e0b837d079626c246bc2ccb2e55cffe137951849))


## v1.0.0 (2023-08-29)

### Features

- Add CDN support
  ([`c4ca397`](https://github.com/eduNEXT/tutor-contrib-mfe-extensions/commit/c4ca397d7014beb4e77db2a1149650f09d20fe12))

This is the first exploration of CDN support for MFEs. We only support the default MFEs used in the
  Olive release and require a custom version of frontend-build and tutor-mfe.
