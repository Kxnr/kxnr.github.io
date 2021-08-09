# kxnr.me

## Description

This is the infrastructure supporting [my website](https://kxnr.me), with dynamic content loading and two factor access control to content.
As I keep notes on projects in a vimwiki, content is written in markdown with vimwiki, registered in a database with 
additional metadata, and rendered to HTML when accessed by a user. The page loader also supports some additional formats,
such as html text, raw text, links, and pdfs. Styles and layouts are included by default, but can straightforwardly be
overridden. This is not, at this point, intended to be a general purpose framework; thus, changes are straightforward but
involve modification to source as opposed to loading resources from configured locations. Required dependencies are minimal,
as outlined below, but are largely limited to flask-security and its dependencies. Some updates to upstream dependencies 
pending, as also noted below.

## Setup

### Dependencies

Due to issues with type handling and default options, I have modified forks of flask-security and passlib. I haven't yet
campaigned for these to be merged into the upstream repositories, though I intend to do this in the near future.

#### Python

* flask-security-too (my [fork](https://github.com/kxnr/flask-security))
  * passlib (my [fork](https://github.com/kxnr/passlib))
* bleach
* sqlalchemy
* click

#### Javascript

* jquery -- by default, this is loaded from a cdn
* pdf.js -- a copy of this library is included in static/js

### Installation

* clone this project ```git clone git@github.com:kxnr/kxnr.me.git```
* setup flask and associated configuration options
  * by default, configuration is loaded from an json formatted file loaded from the FLASK_CONFIG environment variable.
  * I recommend gunicorn and nginx as a reverse proxy, instructions for setup can be found on their respective pages

### Configuration

Configuration is handled by my config module in the pykxnr package. This provides a write once, read only config that can
be frozen to a dictionary and loaded from a file. Top level keys 'common', 'development', and 'production' are expected to
provide shared options, development server options, and production server options, respectively. Within these headers, all
default flask and flask security options are expected. Minimally, this repository requires the following options:

* SECURITY_TOTP_ISSUER
* RESOURCE_KEY
* SQLALCHEMY_DATABASE_URI
* SECURITY_PASSWORD_SALT
* SECRET_KEY
* SECURITY_TOTP_SECRETS

## Help

Setup is effectively unchanged from flask-security setup, for config options, please see documentation for that project.
Otherwise, you're welcome to open an issue or ask a question in this repository and I'll update this document or a pinned
topic with answers to common questions.

## Authors

* [Connor Keane](kxnr.me)

## License

This project is licensed under the GPL3 License - see the LICENSE.md file for details

## Acknowledgments

* The [skeleton CSS](https://github.com/dhg/Skeleton) project by Dave Gamache, which is the base styling for this site
* [pdf.js](https://github.com/mozilla/pdf.js) provided by Mozilla, which drives the embedded pdf viewer
