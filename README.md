# Odoo 12.0 - Technical Training
=======
# Advanced Customization with JS

## Goal

* understand various types of views
* understand FieldWidget API
* modify existing field widgets
* be able to create new field widgets
* be able to create new (non field) widgets

Note: there is no dependency between the various tasks.

## Requirements

- [Widgets](https://github.com/odoo/technical-training/tree/12.0-15-widgets)

## Problem 1: Library Acquisition year

You noticed that the book field 'acquisition_year' is always displayed with a comma: 1,996. This is usually a good formatting for a number, but this is kind of weird for a year. It would be nicer to remove the formatting in that case.  So, let us do that!

## Problem 2: isLate widget in form/kanban views

There is a 'is_late' boolean field on the rental model.  This would be useful to
display in the list/kanban/form view.  Make a new field widget (inheriting from
boolean field), which display a red/green circle, depending if the boolean is true/false.  Also, add it in the list/kanban/form view for rentals.

Bonus point: add options to configure the colors of the widget

## Problem 3: message for some customers

The library management noticed that some customers just forget to pay their dues.   It would be a big help if, each time a new rental is created for one of these customer, there was a message to remind the staff that they should also ask the customer to pay what he owes.

More concretely, in the rental form view, we want to display an information box whenever a customer which owes more than 10 euros is selected. The information box should be in orange if the amount owed is less than 20 euros, and in red if it is more than 20.

## Problem 4: add buttons in control panel

### Geolocation

We have big plans for the future, and these plans involves collecting more data on our customers.  A first step is to make sure we have their GPS coordinates. (note: this task is useful for the 'create a view' module)

- add base_geolocalize as a dependency to the library module
- in the customer form view (and only that one), add a button in the control panel to geolocalize a customer

### Quick payment
In practice, it seems that a common task for the staff is to register a payment for a customer.  To make this operation quicker, we would like to add a button 'Pay Amount Owed' in the control panel of the customer form view.  This button should call a method on the server which will create the appropriate payment, then reload the view.

Bonus points:
- clicking twice on the button should not trigger 2 rpcs
- button should be disabled when customer does not owe any money

## Problem 5: add a systray item

The library purchased a barcode scanner, and want to put it to a good use. They want to be able to scan a customer id, and to quickly navigate to that customer.  Also, the goal is to be able to do that from any screen.

Your task is to add an input in the systray (top menubar), which can be focused, then, when it is filled with a number, will open the form view for the customer.

## Problem 6: Call To Action in Home screen

Since mondays are typically slow days, we have a weekly special promotion to try to ramp up some interest.  It would be nice to add a reminder somewhere in the home screen, so the staff will not forget to get the promotion material out of the closet.

Your task is to add a message in the home screen, somewhere above the application icons. The message should be "Do not forget about Monday promotion", and should obviously only be visible on mondays.

Note: home screen is Enterprise only.  If you use community, put the message in the navbar instead.

## Problem 7: Custom Kanban View (hard)

Your boss had the greatest idea ever: a mix of a Kanban View and a list view would be perfect for your needs!  In a nutshell, he want a list of customers on the left of the rental kanban view.  When you click on a customer on the left, the kanban view on the right is filtered to only display rentals by that customer.

- create an extension of the kanban view and use it in your action
- in your kanbancontroller, do a rpc to fetch the list of all customers which have rented a book
- display the customers in a list on the left of the kanban view
- when you click on a customer on the CustomerList, it should be displayed as selected (maybe change the background), and the kanban view should be filtered accordingly.

Bonus: add a searchbox in the top of the customerlist widget to allow the user to filter on the customer name (note: we have a fuzzy search library somewhere...)

## Resources

### References
* [Abstract Field](https://github.com/odoo/odoo/blob/eb75cb09b5edec9a5569377de7add644a3d989e8/addons/web/static/src/js/fields/abstract_field.js)
* [renderButton method](https://github.com/odoo/odoo/blob/eb75cb09b5edec9a5569377de7add644a3d989e8/addons/web/static/src/js/views/abstract_controller.js#L148)
* [Home screen (app_switcher.js)](https://github.com/odoo/enterprise/blob/38c63d7a5f79ba1bd8f7c5e90d3fe632f202ba37/web_enterprise/static/src/js/app_switcher.js)

### Code samples

* [field registry](https://github.com/odoo/odoo/blob/eb75cb09b5edec9a5569377de7add644a3d989e8/addons/web/static/src/js/fields/field_registry.js)
* [FieldInteger](https://github.com/odoo/odoo/blob/eb75cb09b5edec9a5569377de7add644a3d989e8/addons/web/static/src/js/fields/basic_fields.js#L749)
* [Field widget option](https://github.com/odoo/odoo/blob/fafbc5ebe9ef7c492a691680988e0c9c7a906976/addons/website_event_track/views/event_track_views.xml#L151)

* [Custom View Widget](https://github.com/odoo/odoo/blob/eb75cb09b5edec9a5569377de7add644a3d989e8/addons/web/static/tests/views/form_tests.js#L5921)
* [Adding a systray item](https://github.com/odoo/odoo/blob/eb75cb09b5edec9a5569377de7add644a3d989e8/addons/mail/static/src/js/systray.js#L278)
* [Kanban view extension](https://github.com/odoo/odoo/blob/eb75cb09b5edec9a5569377de7add644a3d989e8/addons/account/static/src/js/account_dashboard_setup_bar.js)
* [Using custom class in a view (js_class attribute)](https://github.com/odoo/odoo/blob/eb75cb09b5edec9a5569377de7add644a3d989e8/addons/account/views/account_dashboard_setup_bar.xml#L8)
