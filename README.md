# Experimental MFE extensions plugin for Tutor

This plugin is meant to be a collection of experimental changes to the
tutor-mfe configuration. At the moment, it will be the testing ground for CDN support
for MFEs.

## Compatibility Table

| Open edX release | Tutor version     | Tutor MFE Version                    | Plugin release |
|------------------|-------------------|--------------------------------------|----------------|
| Nutmeg           | `>=14.0, <15`     | `edunext/tutor-mfe@14.0.2.post1`     | 14.x.x          |
| Olive           | `>=15.0, <16`     | `edunext/tutor-mfe@15.0.7.post2`     | 15.x.x          |

## Installation

```bash
pip install git+https://github.com/edunext/tutor-contrib-mfe-extensions@v15.0.0
pip install git+https://github.com/edunext/tutor-mfe@v15.0.7.post2
```

## Plugin Configuration

- `MFE_EXTENSIONS_CDN_URL` (default: `""`) - The URL of your CDN
  (e.g `https://d1234abcd.cloudfront.net/`)
- `MFE_EXTENSIONS_BY_PATH` (default: `True`) - When enabled will
  add additional routes to caddy to enable routing each mfe through
  a path of the LMS (e.g. `https://{LMS_HOST}/learning`).

## CDN Support

The current deployment of tutor-mfe relies on a webserver
([caddy](https://caddyserver.com/)) to serve the MFE static files directly from
a Docker container. To reduce the amount of IO the server is incurring while
serving a high amount of traffic, we use a CDN to cache the javascript/css
bundles of each MFE and simply serve a small index.html file through caddy.

We use webpack's
[`output.publicPath`](https://webpack.js.org/configuration/output/#outputpublicpath)
to accomplish this. Due to current limitations in the building scripts
we need to use custom versions of `frontend-platform` that include a backport of
[`openedx/frontend-platform#568`](https://github.com/openedx/frontend-platform/pull/568)
for releases previous to Quince.

The following is a list of supported MFEs for the current plugin version, each MFE is a
custom fork hosted by eduNEXT. You might use your own fork, but you must include the backport
mentioned before.

- Learning: [`eduNEXT/frontend-app-learning@ednx-release/olmo.master`](https://github.com/eduNEXT/frontend-app-learning/tree/ednx-release/olmo.master)
- Profile: [`eduNEXT/frontend-app-profile@ednx-release/olmo.master`](https://github.com/eduNEXT/frontend-app-profile/tree/ednx-release/olmo.master)
- Authn: [`eduNEXT/frontend-app-authn@ednx-release/olmo.master`](https://github.com/eduNEXT/frontend-app-authn/tree/ednx-release/olmo.master)
- Account: [`eduNEXT/frontend-app-account@ednx-release/olmo.master`](https://github.com/eduNEXT/frontend-app-account/tree/ednx-release/olmo.master)
- Discussions: [`eduNEXT/frontend-app-discussions@ednx-release/olmo.master`](https://github.com/eduNEXT/frontend-app-discussions/tree/ednx-release/olmo.master)
- Gradebook: [`eduNEXT/frontend-app-gradebook@ednx-release/olmo.master`](https://github.com/eduNEXT/frontend-app-gradebook/tree/ednx-release/olmo.master)
- Ora Grading: [`eduNEXT/frontend-app-ora-grading@ednx-release/olmo.master`](https://github.com/eduNEXT/frontend-app-ora-grading/tree/ednx-release/olmo.master)
- Communications: [`eduNEXT/frontend-app-communications@ednx-release/olmo.master`](https://github.com/eduNEXT/frontend-app-communications/tree/ednx-release/olmo.master)

In addition, we need to use a custom version of `tutor-mfe` that includes the patch
`mfe-dockerfile-production-final` introduced in [`overhangio/tutor-mfe#179`](https://github.com/overhangio/tutor-mfe/pull/179).

### Building Caveats

The value of `publicPath` is fixed at build time, therefore it's not possible to reuse
the MFE docker image if we set it's value to a specific CDN endpoint.
To avoid this limitation we use a script
[`docker-entrypoint.sh`](tutormfe_extensions/templates/mfe/build/mfe/docker-entrypoint.sh)
to dinamically change a placeholder value used in `publicPath` each time the container is
started. The plugin relies on a few Tutor patches that aren't available in Tutor v15 to do this,
for that reason make sure you use the version specified in the Installation section.


Once you enable the plugin you can build an image with a _"dynamic"_ `publicPath`.
By default the placeholder will be replaced by an empty string, which was the original value.
In a Kubernetes environment it will be replaced with the value of `MFE_EXTENSIONS_CDN_URL`.

## Hosting by Path

This plugin adds additional routes to caddy that allows you to serve any MFE defined
by using the `MFE_APP_` variables through the LMS domain using the path:
`https://{LMS_HOST}/{{MFE_CUSTOM_MFE_APP.name}}` where `name` corresponds to the
name variable defined
[on each MFE setting](https://github.com/overhangio/tutor-mfe/blob/v15.0.6/tutormfe/plugin.py#L18).

This is done by using the patch `{{ patch("caddyfile-mfe-by-path") }}` this patch will
add a caddy snippet that will route `/{{MFE_CUSTOM_MFE_APP.name}}` to the MFE container,
by adding this patch to the `caddyfile-lms` patch we can serve the MFE apps through the
LMS domain.

There are several reason why you may want to serve the MFEs through LMS paths instead
of subdomains, the main one is to enable multisite support: instead of using
a single global configuration you can have per-site configuration relying on the
MFE Config API, each MFE can retrieve the configuration of their corresponding LMS
site simply by defaulting to their base domain.

To enable the snippets in your caddy routes make sure `MFE_EXTENSIONS_BY_PATH` is set
to `True` (the default) and if you are using an additional caddy patch to enable
additional routes you can include the `caddyfile-mfe-by-path` patch to your block:

```
    # caddyfile patch
    {$default_site_port} {
        @favicon_matcher {
            path_regexp ^/favicon.ico$
        }
        rewrite @favicon_matcher /theming/asset/images/favicon.ico

        {{ patch("caddyfile-mfe-by-path")|indent(4) }} # Adding this line will include the routes for each MFE.

        # Limit profile image upload size
        request_body /api/profile_images/*/*/upload {
            max_size 1MB
        }
        request_body {
            max_size 4MB
        }
        import proxy "lms:8000"

    }
```

## License

This software is licensed under the terms of the AGPLv3.
