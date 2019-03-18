# Odoo 12.0 - Technical Training
=======
# Computed Fields, Onchange and Constraints

## Goal

The goal of this module is to learn how to have fields interacting with others,
and to automatically compute values based on other fields. This includes:

* computed fields,
* related fields,
* the `depends` decorator,
* storing computed fields in the database,
* onchange triggers,
* constraints.

## Requirements

* [01. Models, Fields and Relations](https://github.com/odoo/technical-training/tree/12.0-01-models/)

## Problem 1: Facilitate Session Registration (OpenAcademy)

In our openacademy module, we already have a few concepts defined: a course and
a session (an instance of a course) containing basic information like the subject,
the instructor, the dates and the room size. To each session, a list of students
that will follow the course can be added.

To help the secretary registrating the attendees, we want to avoid to register
more students than the instructor can take care of. Find one or more ways to
prevent this scenario.

- **Technical Hint**: the computed fields, onchange and constraint do not work
  the same way, are triggered at the same time or serve the same purpose but
  they all can help you.


## Problem 2: Borrow a Book and Be Lazy (Library)

In the first module, we created a basic library module with information on the
book, publisher and customer. When renting a book, we would like to display as
much information as possible on the renting form (about both the customer and
the book) but without having to set this information all over again. Find ways
to be informative and avoids adding workload to the librarians.


## Resources

* [Computed Fields](https://www.odoo.com/documentation/12.0/reference/orm.html#computed-fields)
    * [ORM documentation](https://www.odoo.com/documentation/12.0/reference/orm.html#field-computed)
    * [Depends trigger](https://www.odoo.com/documentation/12.0/reference/orm.html#odoo.api.depends)
    * [Code sample: use the same method for multiple fields](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/point_of_sale/models/pos_order.py#L719)
    * [Code sample: inverse method modifying a distant record](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/delivery/models/delivery_carrier.py#L53)
* [Related Fields](https://www.odoo.com/documentation/12.0/reference/orm.html#related-fields)

* [Onchange](https://www.odoo.com/documentation/12.0/reference/orm.html#onchange-updating-ui-on-the-fly)
    * [The decorator api.onchange](https://www.odoo.com/documentation/12.0/reference/orm.html#odoo.api.onchange)
    * [Code sample: fill contact information](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/hr_recruitment/models/hr_recruitment.py#L228)

* [Constraints](https://www.odoo.com/documentation/12.0/howtos/backend.html#model-constraints)
    * [Python constraints](https://www.odoo.com/documentation/12.0/reference/orm.html#odoo.api.constrains)
        * [Code sample: date verification](https://github.com/odoo/odoo/blob/2021f44c0e053e23d769f1dc2be67b6e3ebed82b/addons/event/models/event.py#L217)
    * [Sql constraints](https://www.odoo.com/documentation/12.0/reference/orm.html#odoo.models.Model._sql_constraints)
        * [Code sample: debit/credit rules](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/account/models/account_move.py#L399)

* [Default values](http://www.odoo.com/documentation/12.0/reference/orm.html#odoo.fields.Field)
    * [Code sample: lunch defaults](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/lunch/models/lunch.py#L29)
