# wagtail-netlify

[![PyPI version](https://badge.fury.io/py/wagtailnetlify.svg)](https://badge.fury.io/py/wagtailnetlify)

Deploy your Wagtail site on Netlify. Features include:

 - the ability to build locally and push them to Netlify, or trigger builds on Netlify's servers
 - (optional) automatic deployment when pages are published
 - an admin UI for viewing and creating Netlify builds
 - a new `netlify` management command
 - conversion of Wagtail redirects to Netlify's format

![Screencast demo](https://tom.s3.amazonaws.com/wagtail-netlify.gif)

## Installation

1. Install and configure [Wagtail Bakery](https://github.com/moorinteractive/wagtail-bakery), if you haven't already.
2. Install [Netlify CLI v2.x](https://www.netlify.com/docs/cli/#installation), if you haven't already.
3. Install Wagtail-Netlify via pip (with `pip install wagtailnetlify`).

## Configuration

1. Add `wagtailnetlify` to your `INSTALLED_APPS`.
2. Run the migrations: `./manage.py migrate wagtailnetlify`.
3. Add `NETLIFY_PATH` or `NETLIFY_BUILD_HOOK` to your settings.

Check the [Settings](#settings) section below for more customisation options.

## Usage

If `NETLIFY_AUTO_DEPLOY` is set to `True`, Wagtail will automatically deploy your site every time a page is published.

*or*

To deploy changes manually, use `./manage.py netlify`. 

To generate redirects without deploying, use the `-n` or `--no-deploy` flag: `./manage.py netlify --no-deploy`. 

To trigger a build on Netlify's servers, configure `settings.NETLIFY_BUILD_HOOK` and use the `-t` or `--trigger-build` flag: `./manage.py netlify --trigger-build`.

## Settings

### `NETLIFY_PATH`

The path to the Netlify CLI. *Hint: type `which netlify` to check the location.*

### `NETLIFY_SITE_ID`

**Default: `None`**

If set, deploy to that specific Netlify site.

If not set, the Netlify CLI might prompt you to select one. This setting is required for the admin view.

### `NETLIFY_API_TOKEN`

**Default: `None`**

If set, the Netlify CLI will not prompt you to click the authentication link in the console. It can be useful when deployed to a remote server where you don't see the console output. This setting is required for the admin view.

Connect to your Netlify account to [generate a token](https://app.netlify.com/account/applications) and then set the settings. *Warning: You should never check credentials in your version control system. Use [environment variables](https://django-environ.readthedocs.io/en/latest/) or [local settings file](http://techstream.org/Bits/Local-Settings-in-django) instead.*

### `NETLIFY_AUTO_DEPLOY`

**Default: `False`**

Whether to automatically deploy your site to Netlify every time you publish a page. This make take between a few seconds and a few minutes, depending on the size of your site, and the number of pages which are affected by your change. If you have configured `settings.NETLIFY_BUILD_HOOK`, publishing a page will trigger a build on Netlify's servers.

### `NETLIFY_DEPLOY_FUNCTION`

**Default: `wagtailnetlify.models.deploy`**

The function to be called when a deploy is triggered (excluding when triggered manually with the `./manage.py netlify` command). It can be useful if you want to use your own task runner (like Celery) instead of the built-in threading model.

The function needs to be a valid [Django signal receiver](https://docs.djangoproject.com/en/2.1/topics/signals/#receiver-functions).

### `NETLIFY_BUILD_HOOK`

**Default: `None`**

The URL of a Netlify build hook. If provided, `./manage.py netlify --trigger-build` will call this hook, triggering a build
on Netlify's servers. This may be useful if you have a headless front-end on Netlify which handles its own static site generation, 
e.g. Nuxt, Next or Gatsby. See https://docs.netlify.com/configure-builds/build-hooks/ for more details.

### Admin view

This view allows Wagtail administrators to see a list of recent Netlify builds, and trigger a new one. Both `NETLIFY_API_TOKEN` and `NETLIFY_SITE_ID` should be available in settings. If `NETLIFY_BUILD_HOOK` has been set, new builds will be created by triggering a build on Netlify's servers; if not, wagtail-netlify will attempt to build the site locally and push it to Netlify.

The view will be available to Wagtail administrators as a new `Netlify` menu item.

### Redirects

Including the `wagtailnetlify` URLs will enable a view at /netlify/redirects, which outputs any Wagtail redirects in [Netlify's plain text format](https://docs.netlify.com/routing/redirects/#syntax-for-the-redirects-file). This may be useful if you are using Netlify to host a headless front-end for your Wagtail site.

To enable this view, update your project's `urls.py`:

```python
# in your imports
from wagtailnetlify import urls as netlify_urls

# in urlpatterns, before including wagtail_urls
url(r"^netlify/", include(netlify_urls)),
```

To include the generated redirects in your Netlify-hosted front-end, you should fetch them from the back-end server as part of your front-end build. For example, for a Nuxt site, the build command could be:

```bash
yarn build && yarn export && wget -O dist/_redirects https://your-wagtail-backend/netlify/redirects
```

## Development

### Releases

1. Ensure you have the latest versions of `pip`, `setuptools` and `twine` installed in your virtual environment.
1. Ensure your `master` branch is up to date.
1. Create a new branch (e.g. `release/v1.1.3`) for the release of the new version.
1. Update the version number in `wagtailnetlify/__init__.py` following [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
1. Update `CHANGELOG.md`.
1. (Optional) If you need to verify anything, use `make publish-test` to upload to https://test.pypi.org and enter your PyPi *test* credentials as needed.
1. On GitHub, create a pull request and squash merge it.
1. Checkout and pull the `master` branch locally.
1. Use `make publish` and enter your PyPi credentials as needed.
1. On GitHub, create a release and a tag for the new version.
