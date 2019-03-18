# Odoo 12.0 - Technical Training
=======
# Business Flow

## Goal

The goal of this module is to learn how to create a business workflow. The learner will be able to

* trigger actions, methods from manual input and depending on specific conditions;
* automate action based on time conditions.


## Requirements

* [Models, Fields and Relations](https://github.com/odoo/technical-training/tree/12.0-01-models)
* [Computed Fields, Onchange and Constraints](https://github.com/odoo/technical-training/tree/12.0-02-fields)
* [Basic Views](https://github.com/odoo/technical-training/tree/12.0-03-views)
* [Model Inheritance](https://github.com/odoo/technical-training/tree/12.0-04-model-inheritance)
* [ORM](https://github.com/odoo/technical-training/tree/12.0-09-orm)


## Problem 1: The Citadel (OpenAcademy)

The citadel is pleased with the way Odoo allows the Archmaesters to have more
time to take care of their ravens, which are the only trustworthy way of
communicating in all Westeros.

They have noticed that, in the current state of the system, the sessions are all
considered equal. They would like to differentiate sessions that are in
preparation from those that are ready to be given. They would love to have a way
to automatically set sessions as confirmed when you have at least 50% of the
seats filled.

The Maesters would grant you an additional link to your chain if the instructor
and teacher involved could be notified and keep an history of those
notifications. They heard about something called the chatter...


## Problem 2: Library management

Brussels' library uses Odoo to manage their customers and books. Their module
has been built on top of existing modules: for modeling the books, they
inherited the model `product.product`, and for the customers, authors and
publishers, they inherited the model `res.partner`.

They would like to enhance the system: they want to manage the payments of the
customers, what they owe. For regular payments, depending on the length of the
rental, but also a fine when the book is never returned and is lost. To avoid
having to manage the rental, the books and the customers everywhere, it would be
neat to trigger most of the actions from the rental form view. The total amount
owed should be visible on the customer's form view and should be searchable.

- **Hint**: To manage the time, you can use methods defined on the Date field.

#### Extra task

* The librarians know that most of the time, people just forget about a rented
  book, so they would like to have a reminder mechanism to notify the customer.


## Resources

### Reference


* [Status bar](http://www.odoo.com/documentation/12.0/reference/views.html#the-status-bar)
* [Recordset operations](http://www.odoo.com/documentation/12.0/reference/orm.html#other-recordset-operations)
* [Environment](http://www.odoo.com/documentation/12.0/reference/orm.html#environment)
* [Online Tutorial](http://www.odoo.com/documentation/12.0/howtos/backend.html#build-an-odoo-module)

### Code Sample

* [Form buttons](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/account/views/account_invoice_view.xml#L220)
* Chatter example:
  - [Model](https://github.com/odoo/odoo/blob/d9235a8f14a2dbd23a5640ffd1ec6bef4f235640/addons/sale/models/sale.py#L22)
  - [View](https://github.com/odoo/odoo/blob/d9235a8f14a2dbd23a5640ffd1ec6bef4f235640/addons/sale/views/sale_views.xml#L398)
* [Date field information](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/odoo/fields.py#L1447)
* [Email template](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/event/data/email_template_data.xml)
* [Send Email template](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/event/models/event.py#L275)
* [Cron](https://github.com/odoo/odoo/blob/ab5fcb29650349fa641c6130bf6dcbdc1ec28a07/addons/membership/data/membership_data.xml)
