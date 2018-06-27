# wagtail-netlify

Deploy your Wagtail site on Netlify. Features include:

 - automatic deployment when pages are published
 - a new `netlify` management command
 - conversion of Wagtail redirects to Netlify's format

![Screencast demo](https://tom.s3.amazonaws.com/wagtail-netlify.gif)

## Install

1. Install and configure [Wagtail Bakery](https://github.com/moorinteractive/wagtail-bakery), if you haven't already
2. Install [Netlify](https://www.netlify.com/docs/cli/#installation), if you haven't already
3. Install the project with `pip install wagtailnetlify`.

## Configure

### Mandatory
1. Add `'wagtailnetlify'` to your `INSTALLED_APPS`
2. Run the migrations: `./manage.py migrate wagtailnetlify`
3. Add `NETLIFY_PATH` to your settings (hint: type `which netlify` to check the location)

### Optional
- If you are deploying to an existing Netlify site, provide its ID with `NETLIFY_SITE_ID = 'your-id-here'`
- If you don't want Wagtail to deploy your site to Netlify every time you publish a page, set `NETLIFY_AUTO_DEPLOY = False`
- If you don't want to or are unable to click the Netlify authentication link in the console, [generate a token](https://app.netlify.com/account/applications) manually and set `NETLIFY_API_TOKEN = 'your-token-here'` in your settings. *Warning: You should never check credentials in your version control system. Use [environment variables](https://django-environ.readthedocs.io/en/latest/) or [local settings file](http://techstream.org/Bits/Local-Settings-in-django) instead.*

## Usage

1. If you haven't set `NETLIFY_AUTO_DEPLOY = False`, Wagtail will automatically deploy your site every time a page is published. This make take between a few seconds and a few minutes, depending on the size of your site, and the number of pages which are affected by your change.
2. To deploy changes manually, use `./manage.py netlify`

## Optional admin view

Netlify can send a webhook after a successful deployment. This app provides an endpoint for that webhook and an admin view of
completed deployments. To enable this view, add `'wagtail.contrib.modeladmin'` to your `INSTALLED_APPS` and update your project's `urls.py`:

```python
# in your imports
from wagtailnetlify import views as netlify_views

# in urlpatterns, before including wagtail_urls
url(r'^netlify/', netlify_views.success_hook, name='netlify'),
```

In Netlify's admin interface for your app, add http://yourdomain/netlify/success as a URL to notify for the outgoing webhook on 'Deploy succeeded' events (in Settings / Build & deploy / Deploy notifications).

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
