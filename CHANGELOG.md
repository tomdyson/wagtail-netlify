# Changelog

All notable changes to this project will be documented in this file.

...

## v0.8

Significant update, with backwards-incompatible changes. 
The `Deployment` model has been removed, in favour of direct 
integration with the Netlify API. A new view for Wagtail 
administrators lists the last ten builds, with the option of 
triggering new builds.

### Added

- Admin UI integration with the Netlify build API

### Removed

- Support for Wagtail < 2

## v0.7

### Added

- Support triggering builds on Netlify automatically

## v0.6

### Added

- A command option for triggering builds on Netlify

## v0.5

### Added

- A view for exposing redirects in Netlify's plain text format

## v0.4

### Added

- support for generating redirects without deploying

## v0.3

### Added

- Netlify-cli 2.x compatibility #13
- Possibility to define custom deployments function #8

### Removed

- Netlify-cli 1.x compatibility #13

## v0.2

### Added

- Wagtail 2.0 compatibility #4

### Fixed

- Prevent modification of Deployment objects #2
- Prevent registration of Deployment modeladmin when the modeladmin app isn't installed #3

## v0.1

Initial Release
