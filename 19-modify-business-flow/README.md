# Modify Business Flows

## Goal

In this module, you will learn to modify existing business flows.

## Requirements

* [Model Inheritance](../04-model-inheritance)
* [View Inheritance](../05-view-inheritance)


## Problem 1: Double Validation on Sales Orders

Create a small module that depends on the module `sale`. The module should add a
double validation process on sales orders: the sales user first confirms their
sales order, then a sales manager double-confirm it. Add an extra possible value
for the field `state` on model `sale.order`, and modify the buttons on the sales
order form. The first confirmation put the sales order in your extra state. The
second confirmation should assign the sales order to the state `sale`.

### References

* [Sales Order Model](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/sale/models/sale.py#L15)
* [Sales Order Form View](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/sale/views/sale_views.xml#L142)
* [Selection Fields](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/odoo/fields.py#L1625)


## Problem 2: Close an Issue with a URL

Project issues already provide email feedback to their customer. Currently, the
email received by the customer of an issue already provides links to view the
issue, etc. Add a link inside the email that closes the issue upon click.

When a links in the email is clicked, the url is resolved by an HTTP controller
in the Odoo server. The controller is a method that may execute some business
code thanks to the Odoo ORM, and it may return a response that renders an HTML
template.

Note that creating a new controller is not really necessary: you may use the
existing controllers to achieve what you want (see references below.) Make it
call a method that checks the issue's field `stage_id`, and modifies it.

### References

* [Add Links in Email](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/project_issue/models/project_issue.py#L229)
* [Generate URL for Action](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/mail/models/mail_thread.py#L559)
* [Process URL in Controller](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/mail/controllers/main.py#L198)


## Problem 3: Detect Time Overtaking on Tasks

When a user encodes some timesheet for a project task, the remaining hours are
computed on the task. If the user encodes more hours than the task's planned
hours, it may be a sign of a problem on the task. In that case, an email should
be sent to the user's manager.

### References

* [Timesheets](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/hr_timesheet/hr_timesheet.py#L7)
* [Timesheets on Tasks](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/hr_timesheet/project_timesheet.py#L15)
