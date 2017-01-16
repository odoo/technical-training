# Action, Wizard and Context

## Goal

- return action from a button, add an action in more menu
- create wizard
- stat/smart button

## Requirements


- [Models, Fields and Relations](../01-models)
- [Computed Fields, Onchange and Constraints](../02-fields)
- [Basic Views](../03-views)

## Problem 1: The Citadel (OpenAcademy)

In order to see who followed a course, we want to add a smart button on the `course`
form to see the amount of participants and when and redirect to the list of participant
of any `session`.

Also, to accelerate the registration to a session, from the the `res.partner` tree view,
you can select participant and add them in a session in the `more` via a wizard to select
the correct session.

## Problem 02: Library Management

The librarian want to see who has ever rented a book as well as the count directly on
the book form via a smart button. Also he wants to be able to select books to create a rental
for a `res.partner` via a 2 level wizard:
* Level 1: select books
* Level 2: Select partner and see all the books he rented


## Resources

### Reference

* [Wizard](https://www.odoo.com/documentation/10.0/howtos/backend.html#wizards)
* [Launching wizard](https://www.odoo.com/documentation/10.0/howtos/backend.html#launching-wizards)

### Code Sample

* [Return action in Python](https://github.com/odoo/odoo/blob/10.0/addons/mrp_repair/wizard/mrp_repair_make_invoice.py#L26)