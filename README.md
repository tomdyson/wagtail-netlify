# wagtail-netlify

[![PyPI version](https://badge.fury.io/py/wagtailnetlify.svg)](https://badge.fury.io/py/wagtailnetlify)

Deploy your Wagtail site on Netlify. Features include:

 - automatic deployment when pages are published
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
3. Add `NETLIFY_PATH` to your settings.

Check the [Settings](#settings) section below for more customisation options.

## Usage

If `NETLIFY_AUTO_DEPLOY` is set to `True`, Wagtail will automatically deploy your site every time a page is published.

*or*

To deploy changes manually, use `./manage.py netlify`.

## Settings

### `NETLIFY_PATH`

The path to the Netlify CLI. *Hint: type `which netlify` to check the location.*

### `NETLIFY_SITE_ID`

**Default: `None`**

If set, deploy to that specific Netlify site.

If not set, the Netlify CLI might prompt you to select one.

### `NETLIFY_API_TOKEN`

**Default: `None`**

If set, the Netlify CLI will not prompt you to click the authentication link in the console. It can be useful when deployed to a remote server where you don't see the console output.

Connect to your Netlify account to [generate a token](https://app.netlify.com/account/applications) and then set the settings. *Warning: You should never check credentials in your version control system. Use [environment variables](https://django-environ.readthedocs.io/en/latest/) or [local settings file](http://techstream.org/Bits/Local-Settings-in-django) instead.*

### `NETLIFY_AUTO_DEPLOY`

**Default: `True`**

Whether to automatically deploy your site to Netlify every time you publish a page. This make take between a few seconds and a few minutes, depending on the size of your site, and the number of pages which are affected by your change.

### `NETLIFY_DEPLOY_FUNCTION`

**Default: `wagtailnetlify.models.deploy`**

The function to be called when a deploy is triggered (excluding when triggered manually with the `./manage.py netlify` command). It can be useful if you want to use your own task runner (like Celery) instead of the built-in threading model.

The function needs to be a valid [Django signal receiver](https://docs.djangoproject.com/en/2.1/topics/signals/#receiver-functions).

### Optional admin view

Netlify can send a webhook after a successful deployment. This app provides an endpoint for that webhook and an admin view of completed deployments. To enable this view:

1. Add `wagtail.contrib.modeladmin` to your `INSTALLED_APPS`
1. Update your project's `urls.py`:

```python
# in your imports
from wagtailnetlify import views as netlify_views

# in urlpatterns, before including wagtail_urls
url(r'^netlify/', netlify_views.success_hook, name='netlify'),
```

3. In Netlify's admin interface for your app, add http://yourdomain/netlify/success as a URL to notify for the outgoing webhook on *Deploy succeeded* events (in Settings / Build & deploy / Deploy notifications).

The view will be available under `Settings / Deployments` in your site's admin.

## Development

### Releases

1. Ensure you have the latest versions of `pip`, `setuptools` and `twine` installed in your virtual environment.
1. Create a new branch (e.g. `release/v1.1.3`) for the release of the new version.
1. Update the version number in `wagtailnetlify/__init__.py` following [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
1. Update `CHANGELOG.md`.
1. On GitHub, create a pull request and squash merge it.
1. Checkout and pull the `master` branch locally.
1. (Optional) If you need to verify anything, use `make publish-test` to upload to https://test.pypi.org and enter your PyPi *test* credentials as needed.
1. Use `make publish` and enter your PyPi credentials as needed.
1. On GitHub, create a release and a tag for the new version.
