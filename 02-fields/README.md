# Fields decorators and attributes

## Goal

The goal of this module is to learn how to have fields interacting with others
and to automatically compute values based on other fields. This includes:

* computed field
* related fields
* depends attribute
* storing in the database
* onchange triggers
* constraints

## Requirements

* [01. Models](../01-models/)

## Problem 01: facilitate session registration

In our openacademy module, we already have a few concepts defined: a course and
a session (an instance of a course) containing basic information like the subject,
the instructor, the dates and the room size. To each session, a list of students
that will follow the course can be added.

To help the secretary registrating the attendees, we want to avoid to register
more students than the instructor can take care of. Find one or more way to
prevent this scenario.

- **directory** : [02-fields/ex01](./ex01/)
- **Technical Hint**: the computed fields, onchange and constraint do not work
  the same way, are triggered at the same time or serve the same purpose but
  they all can help you.

## Problem 02: borrow a book and being lazy

In the first module, we created a basic library module with information on the
book, publisher and customer. When renting a book, we would like to display as
much information as possible on the renting form (about both the customer and
the book) but without having to set this information all over again. Find ways
to be informative and avoids adding workload to the librarians.

- **directory** : [02-fields/ex02](./ex02/)

## Resources

### Computed fields

* [Computed fields](https://www.odoo.com/documentation/9.0/reference/orm.html#computed-fields)
    * [ORM doc](https://www.odoo.com/documentation/9.0/reference/orm.html#field-computed)
    * [Depends trigger](https://www.odoo.com/documentation/9.0/reference/orm.html#openerp.api.depends)
    * [Code sample: use the same method for multiple fields](https://github.com/odoo/odoo/blob/a4378111/addons/point_of_sale/point_of_sale.py#L1485)
    * [Code sample: inverse method modifying a distant record](https://github.com/odoo/odoo/blob/a4378111/addons/delivery/models/delivery_carrier.py#L53)
* [Related field](https://www.odoo.com/documentation/9.0/reference/orm.html#related-fields)

### Onchange

* [Onchange](https://www.odoo.com/documentation/9.0/reference/orm.html#onchange-updating-ui-on-the-fly)
* [api.onchange decorator](https://www.odoo.com/documentation/9.0/reference/orm.html#openerp.api.onchange)
* [Code sample: fill contact information](https://github.com/odoo/odoo/blob/a4378111/addons/hr_recruitment/models/hr_recruitment.py#L244)

### Constraints

* [Model constraints tutorial](https://www.odoo.com/documentation/9.0/howtos/backend.html#model-constraints)
* [python constraint](https://www.odoo.com/documentation/9.0/reference/orm.html#openerp.api.constrains)
    * [Code sample: date verification](https://github.com/odoo/odoo/blob/a4378111/addons/event/models/event.py#L203)
* [sql constraint](https://www.odoo.com/documentation/9.0/reference/orm.html#openerp.models.Model._sql_constraints)
    * [Code sample: debit/credit rules](https://github.com/odoo/odoo/blob/a4378111/addons/account/models/account_move.py#L406)

### Default value

* [ORM default attribute](http://www.odoo.com/documentation/9.0/reference/orm.html#openerp.fields.Field)
* [Code sample: lunch defaults](https://github.com/odoo/odoo/blob/a4378111/addons/lunch/models/lunch.py#L28)
