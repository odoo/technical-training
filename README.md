# Odoo 12.0 - Technical Training
=======
# Model Inheritance

## Goal

Odoo provides two *inheritance* mechanisms to extend an existing model in a
modular way. With the Odoo inheritance mechanims, you can:

- add or override fields, methods, constraints on an existing model;
- factor out some generic code in model mixins;
- associate each records from a model with a *parent record* from another model.

The purpose of this module is to learn these inheritance mechanisms.


## Requirements

- [Models, Fields and Relations](https://github.com/odoo/technical-training/tree/12.0-01-models)
- [Computed Fields, Onchange and Constraints](https://github.com/odoo/technical-training/tree/12.0-02-fields)
- [Basic Views](https://github.com/odoo/technical-training/tree/12.0-03-views)


## Problem 1: Instructors (OpenAcademy)

We assume that both session instructors and session attendees relate to the
general model for contacts, namely `res.partner`. The model fits well for
attendees, but is not specific enough for instructors: not every contact may be
assigned as instructor for a session.

Extend the model `res.partner` with a boolean field `instructor`, which allows
to distinguish between instructors and other contacts. Also add a read-only
field that shows the sessions attended by a given contact. Modify the instructor
field on sessions such that only contacts marked as instructors can be selected.

In the given code, a menu and specific views are defined for contacts in the
context of courses. Modify the views to show the new fields. There exists
another, modular way of modifying views, but this is the subject of the training
module [View Inheritance](../05-view-inheritance).

- **Hint**: Use a *domain* on relational fields to restrict which records may be
  selected


## Problem 2: Library Management

With our application, Brussel's library can now manage the rentals of books by
customers. However, the librarians are not happy with the solution. The library
usually has several copies of a given book, which makes the list of books full
of redundant data. Moreover, they want to identify each copy of a book with a
unique reference, which is internal to the library. Rentals should relate to the
actual book copy that is borrowed.

Add a specific data model for book copies. All the copies of a book should share
the same, unique, book data (title, authors, ISBN, etc.) Every book copy should
have a unique internal reference. Rentals should relate to book copies instead
of books.

- **Hint**: Use delegation inheritance for book copies.


## Resources

### Reference

* [Inheritance and Extension](http://www.odoo.com/documentation/11.0/reference/orm.html#reference-orm-inheritance)
* [Domains](http://www.odoo.com/documentation/11.0/reference/orm.html#domains)
* [Basic Fields Documentation](http://www.odoo.com/documentation/11.0/reference/orm.html#basic-fields)
* [Online Tutorial](http://www.odoo.com/documentation/11.0/howtos/backend.html#inheritance)

### Code Sample

* [Add fields to a model](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/account/models/product.py#L7)
* [Override a method on a model](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/account/models/product.py#L39)
* [Create a model by extending another model](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/account/models/res_config.py#L14)
* [Use abstract models as mixins](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/product/models/product_template.py#L15)
* [Product variants](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/product/models/product.py#L106)
