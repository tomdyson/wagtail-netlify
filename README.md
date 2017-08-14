# wagtail-netlify

Deploy your Wagtail site on Netlify, automatically.

## Install

1. Install and configure [Wagtail Bakery](https://github.com/moorinteractive/wagtail-bakery), if you haven't already
2. Install [Netlify](https://www.netlify.com/docs/cli/#installation), if you haven't already
3. `pip install git+https://github.com/tomdyson/wagtail-netlify.git`

## Configure

1. Add `'wagtailnetlify'` to your INSTALLED_APPS
2. Add `NETLIFY_PATH` to your settings (hint: type `which netlify` to check the location)
3. If you are deploying to an existing Netlify site, provide its ID with `NETLIFY_SITE_ID = 'your-id-here'`
4. If you don't want Wagtail to deploy your site to Netlify every time you publish a page, set `NETLIFY_AUTO_DEPLOY = False`

## Usage

1. If you haven't set `NETLIFY_AUTO_DEPLOY = False`, Wagtail will automatically publish your site every time a page is published. This make take between a few seconds and a few minutes, depending on the size of your site, and the number of pages which are affected by your change.
2. To deploy changes manually, use `./manage.py netlify`

## Todo

- [ ] Provide an admin view for reporting on deployments
- [ ] Allow developers to replace `Threading` with Celery or similar, for more robust async behaviour.
- [ ] Tests