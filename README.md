# Experimental MFE extensions plugin for Tutor

This plugin is meant to be a collection of experimental changes to the
tutor-mfe configuration. At the moment, it will be the testing ground for CDN support
for MFEs.

## Compatibility Table

| Open edX release | Tutor version     | Tutor MFE Version                    | Plugin release |
|------------------|-------------------|--------------------------------------|----------------|
| Olive            | `>=15.0, <16`     | `edunext/tutor-mfe@15.0.7.post1`     | 1.x.x          |

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
the 7 default MFEs in olive:

- account: `v12.0.6-cdn-support`
- course-authoring: `v11.0.2-cdn-support`
- discussions: `v11.0.2-cdn-support`
- authn: `v11.0.2-cdn-support`
- gradebook: `v9.1.4-cdn-support`
- learning: `v9.1.4-cdn-support`
- profile: `v12.0.6-cdn-support`

In addition, we need to use a custom version of `tutor-mfe` to set extra environment
variables before the build step. The custom version version of `tutor-mfe` is going
to be needed for Olive installations and will eventually be dropped some time during
the Palm release.

### Building Caveats

At the moment each MFE image will be tied to a specific CDN endpoint. As a result,
it isn't possible to reuse the MFE image between environments (namely Staging and
production). You will have to rebuild the image in the following scenarios:

1. You have a working production image and want to enable CDN support: You must rebuild the image using the same parameters while setting the  `MFE_EXTENSIONS_CDN_URL` variable with your distribution.
2. You modified your CDN endpoint and it now uses a different URL: Update the value of `MFE_EXTENSIONS_CDN_URL` to the new URL.
3. You made changes to the code of any of the MFEs in the image and want to deploy a new version: If your configuration already had CDN support update the other parameters as you usually do in your deployment process, if it didn't have CDN suppport follow step #1.


## License

This software is licensed under the terms of the AGPLv3.
