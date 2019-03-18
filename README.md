# Odoo 12.0 - Technical Training
=======
# Play with the ORM

## Goal

* Be able to find and use the ORM methods
* Be able to find the signature of a ORM method
* Be able to use the odoo shell


## Requirements

- [Models, Fields and Relations](https://github.com/odoo/technical-training/tree/12.0-01-models)
- [Computed Fields, Onchange and Constraints](https://github.com/odoo/technical-training/tree/12.0-02-fields)


## Problem 1: Retrieve Model Information

During your development, you want to use the country code on the model
`res.country`, but you don't know whether this field already exists. The goal of
this exercise is to find information about the fields of model `res.country`.

###  Hint

* Use the Odoo shell subcommand: `odoo shell`.
* Instantiate the model from the environment object: `env['res.country']`.
* Retrieve field information with method `fields_get`.


## Problem 2: Openacademy

Session instructors are given by contact records, specifically from the model
`res.partner`. Add a button on sessions to create an invoice for the instructor
of the session. There should be only one invoice per instructor; if the invoice
already exists, add a line to the existing invoice.


### Extra

Once the invoice line has been created, mark the session as paid (see field
`is_paid`.) The button should not be visible when the session is paid.


## Problem 3: Planing Management

Change the way a task type is shown in relation fields, i.e., its label or
"display name". The label should combine the task type name and its description.
Make sure that a task type can be found by searching on parts of its name or
description.


## References

* [The ORM API](https://www.odoo.com/documentation/12.0/reference/orm.html)
* [The Code of the ORM](https://github.com/odoo/odoo/blob/12.0/odoo/models.py)
