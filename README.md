# kxnr.me

## Description

This is the infrastructure supporting [my website](https://kxnr.me), written in early 2020 and, 
surprisingly, still functioning. As with any project, it is showing its age as both I and the 
software industry have progressed. I'll be updating this project to `FastAPI`, likely, a wasm
framework for the front end


## Setup

### Configuration

This app loads configuration from a json file, whose filename is expected in the `FLASK_CONFIG` env
variable. In addition to standard flask configuration, this app requires values for the following
variables:

* SECURITY_TOTP_ISSUER
* RESOURCE_KEY
* SQLALCHEMY_DATABASE_URI
* SECURITY_PASSWORD_SALT
* SECRET_KEY
* SECURITY_TOTP_SECRETS

### Management

Management of website users and content are run through click commands. Available commands can be seen with `flask help`.
For this project, there are three levels of management available: Content, Category, and Role. The content describes
individual components along with metadata and can be managed through `flask content` subcommands. 

Categories can be used 
to control rendering of pages or access to pages. Pages may belong to multiple categories, and all pages in a category may
be loaded by accessing the category. Categories may also be added as a render option to Content, which will render a preview
of the pages in the Category. Categories can be modified with `flask category` subcommands. 

Roles control access to Content and are applied as a filter on all queries. Roles are currently exposed through the
flask-security command line interface, so please check that project for user management commands.

## Authors

* [Connor Keane](kxnr.me)

## License

This project is licensed under the GPL3 License - see the LICENSE.md file for details

## Acknowledgments

* The [skeleton CSS](https://github.com/dhg/Skeleton) project by Dave Gamache, which is the base styling for this site
* [pdf.js](https://github.com/mozilla/pdf.js) provided by Mozilla, which drives the embedded pdf viewer
