# Business flow

## Goal

The goal of this module is to learn how to create a business workflow. The learner will be able to:

* Trigger actions, methods from manual input and depending on specific conditions
* Automate action based on time conditions

## Requirements

* [01. Models](../01-models/)
* [02. Fields](../02-fields/)
* [03. Views](../03-views/)
* [04. Model Inheritance](../04-model-inheritance/)
* [09. Orm](../02-orm/)

## Problem 01: Citadel

The citadel is pleased with the way odoo allows the Archmaesters to have more time to take care of their ravens which are the only trustworthy way of communicating in all Westeros. They've noticed that in the current state of the system, the sessions are all considered equal, they would like to be able to differentiate session that are in preparation to those who are ready to be given. They would love to have a way to automatically set sessions as confirmed when you have at least 50% of the seats filled. The Maesters would grant you an addtional link to your chain if the instructor and teacher involved could be notified and keep an history of those notifications, they heard about something called the chatter.


## Problem 02: Library management

Brussels' library uses odoo to manage their customers and the books. Their module has been built on top of existing modules: to modelise the books, they inherited the product.product model and the customers, authors and publishers inherit the model res.partner. They would like to enhance their existing system: they want to be able to manage the payments of the customers, what they owe: for regular payments depending on the length of the rental but also a fine when the book is never returned and is lost. To avoid having to manage, the rental, the books and the customer everywhere, it would be neat to be able to trigger most of the actions from the rental form view. The total amount owed would be visible on the customers and should be searchable.

- **Hint**: To manage the time, you can use methods defined on the date field.

#### Extra task

* The librarians know most of the time people just forget about the rented book, so they would like to have a reminding mechanism to notify the customer.


## Resources

### Reference


* [Status bar](http://www.odoo.com/documentation/9.0/reference/views.html#the-status-bar)
* [Recordset operations](http://www.odoo.com/documentation/9.0/reference/orm.html#other-recordset-operations)
* [Environment](http://www.odoo.com/documentation/9.0/reference/orm.html#environement)
* [Online Tutorial](http://www.odoo.com/documentation/9.0/howtos/backend.html#build-an-odoo-module)

### Code Sample

* [Form buttons](https://github.com/odoo/odoo/blob/d88aa53/addons/account/views/account_invoice_view.xml#L217)
* [Chatter example](https://github.com/odoo/odoo/blob/d88aa53/addons/event/views/event_views.xml#L136)
* [Date field information](https://github.com/odoo/odoo/blob/d88aa53/openerp/fields.py#L1335)
* [Email template](https://github.com/odoo/odoo/blob/d88aa53/addons/event/data/email_template_data.xml)
* [Send Email template](https://github.com/odoo/odoo/blob/d88aa53/addons/event/models/event.py#L260)
* [Cron](https://github.com/odoo/odoo/blob/d88aa53/addons/membership/membership_data.xml)
