# Models, Fields and Relations

## Goal

The goal of this module is to learn how the models/objects in Odoo are defined
and how they interact with each other. The learner will be able to:

* translate a simple situation into models that will fit the Odoo framework;
* define a simple model;
* define simple fields on a model;
* define relational fields between models.

## Requirements

* [Python](https://www.python.org/)

## Problem 1: The Citadel (OpenAcademy)

The citadel of the seven kingdoms, located in Oldtown would like to use Odoo to
manage the training of its future maesters. In this system, the citadel wants to
create and edit classes, with different levels. They would like to handle
different sessions given by different maesters at different moments. It would be
nice to register the attendees of those sessions. Maester Aemon thinks it would
be a good idea to differentiate the sessions in preparation from the ones that
will actually be given, as well as having a way to archive the sessions, so they
can find what they need as quickly as you can find a book in the Citadel's
Library, which is the largest in Westeros.

- **Hint**: To have access to the models in the UI, you can add a menu from the
  models table in the UI in debug mode (go to Settings/Technical/Models, pick
  your model and click on Create a Menu).
- **Technical Hint**: Do not forget to import the `api`, `models` and `fields`
  and your different files

#### Extra task

* When removing a course, you don't want to have orphan sessions left in the
  system, as the library, it has to be nice and clean.


## Problem 02: Library Management

Brussels' library wants to use Odoo to manage their books and customers. The
librarians want to record new books, with the standard information: authors,
editors, year of edition, ISBN, etc. For their customers, they want to manage
them, create a new one, and include some standard information like name,
address, emails, and other information. They want to visualize what customers
rented on their profile, as well as seeing the customers on the books without
being able to change it.

- **Hint**: You want to be able have multiple authors for a book.
- **Hint**: You want to be able to have customers renting multiple books.

#### Extra task

* The librarians wants to be able to have the history of the book rentals, with
  the rental date and the return date.


## Problem 03: Cooperative Volunteers

A non profit organisation needs your help. They would like to use Odoo to
organize the work of their volunteers. They are managing a cooperative shop
selling local products. The cooperative split all the work in smaller tasks that
are coming every week like loading a truck, handling the point of sale,
distributing the goods, etc. The have various type of volunteers, some are able
to take responsibilities for recurring tasks, some can only take over a task
every now and then. Not every task can be handled by only one person. In the
end, every job has to be done.

They would like to have a system in which they can check day-to-day if they have
enough volunteers. They would have recurring tasks and one-shot tasks handled by
their volunteers. For now you can assume that every volunteer handles the task
in a recurring way 2-3 hours per week at a time.


## Resources

### Reference

* [Activate Debug Mode](https://www.odoo.com/documentation/11.0/howtos/web.html#a-simple-module)
* [Models Documentation](http://www.odoo.com/documentation/11.0/reference/orm.html#model-reference)
* [Basic Fields Documentation](http://www.odoo.com/documentation/11.0/reference/orm.html#basic-fields)
* [Relational Fields Documentation](http://www.odoo.com/documentation/11.0/reference/orm.html#relational-fields)
* [Online Tutorial](http://www.odoo.com/documentation/11.0/howtos/backend.html#build-an-odoo-module)

### Code Sample

* [API stuff to import](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/odoo/addons/base/res/res_bank.py#L5)
* [Simple model with some basic fields](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/odoo/addons/base/res/res_bank.py#L15)
* [Many2one](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/sale/models/sale.py#L701)
* [One2many](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/sale/models/sale.py#L128)
* [Many2many](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/account/models/product.py#L25)
