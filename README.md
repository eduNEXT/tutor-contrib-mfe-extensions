# Experimental MFE extensions plugin for Tutor

This plugin is meant to be a collection of experimental changes to the
tutor-mfe configuration. At the moment, it will be testing ground for CDN support
for MFEs.


## Installation

```bash
pip install git+https://github.com/edunext/tutor-contrib-mfe-extensions@v1.0.0#egg=tutor-contrib-mfe-extensions==v1.0.0
pip install git+https://github.com/edunext/tutor-mfe@v15.0.7.post1#egg=tutor-mfe==v15.0.7.post1
```

## Plugin Configuration

- `MFE_EXTENSIONS_CDN_URL` (default: `""`) - The URL of your CDN
  (e.g `https://d1234abcd.cloudfront.net/`)

## CDN Support

The current deployment of tutor-mfe relies on a webserver
([caddy](https://caddyserver.com/)) to serve the MFE static files directly from
a Docker container. To reduce the amount of IO the server is incurring while
serving a high amount of traffic, we use a CDN to cache the javascript/css
bundles of each MFE and simply serve a small index.html file through caddy.

We use webpack's
[`output.publicPath`](https://webpack.js.org/configuration/output/#outputpublicpath)
to accomplish this. Due to current limitations in the building scripts
we need to use a custom version of
[`frontend-build`](https://github.com/eduNEXT/frontend-build/branches/all?query=cdn).
Until [`openedx/frontend-build#398`](https://github.com/openedx/frontend-build/pull/398)
is merged.

There is a custom version for each major release of `frontend-build` used by
the 6 default MFEs in olive:

- account: `v12.0.6-cdn-support`
- course-authoring: `v11.0.2-cdn-support`
- discussions: `v11.0.2-cdn-support`
- authn: `v11.0.2-cdn-support`
- gradebook: `v9.1.4-cdn-support`
- learning: `v9.1.4-cdn-support`
- profile: `v12.0.6-cdn-support`

Because the `tutor-mfe` doesn't allow setting arbitrary ENV variables before
build time we need to install a custom version during the olive release.

## License

This software is licensed under the terms of the AGPLv3.
