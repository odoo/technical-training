# Odoo 12.0 - Technical Training
=======
# Controllers

## Goal

* Be able to create a controller with a specific route
* Be able to use a controller and return a response with a useable format

## Requirements

- [Models, Fields and Relations](https://github.com/odoo/technical-training/tree/12.0-01-models)
- [Computed Fields, Onchange and Constraints](https://github.com/odoo/technical-training/tree/12.0-02-fields)
- [Play with the ORM](https://github.com/odoo/technical-training/tree/12.0-09-orm)
- [Reports](https://github.com/odoo/technical-training/tree/12.0-10-reports)

## Problem 1: Library :

The library has decided to extend what their customer can access online. Create a web page for users to rent a book directly from the website. You can
rent a given book only if nobody has rented this book before you.

## Problem 2: Citadel (openAcademy)

The academy wants to allow anybody to see general information on courses and sessions on their website through precises urls.  Create pages to display sessions and courses, and link them to alllow navigation on the website.  Please remember that no confidential information shall be displayed on a public page !

## References

* [URL and routing](http://www.odoo.com/documentation/11.0/howtos/website.html#urls-and-routing)

### Code Sample

* [Controller](https://github.com/odoo/odoo/blob/10.0/addons/website_blog/controllers/main.py#L19)
* [Route](https://github.com/odoo/odoo/blob/10.0/addons/website_sale/controllers/main.py#L180)
