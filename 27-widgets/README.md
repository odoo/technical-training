# Advanced Widgets

## Goal

* Be able to add 'smart' buttons.
* Be able to create a new stat button.
* Be able to customize a field with different widgets.

## Requirements

* [Models, Fields and Relations](../01-models)
* [Computed Fields, Onchange and Constraints](../02-fields)
* [Basic Views](../03-views)
* [Model Inheritance](../04-model-inheritance)
* [ORM](../09-orm)
* [Mail Integration](../25-mail-integration)


## Problem 1: Fields with a Better Look (OpenAcademy)

We already have created a session model and a course model. Then we created
different views (form, tree, search, etc.). In these views we focused on the
content (fields) without worrying too much about their aspect.

We would like to improve the look of the field `level` on courses. This field is
a selection field, and we want to see a radio button in place of a dropdown.

#### Extra Task

You also want to be able to drag and drop sessions depending on their sequence.


## Problem 2: Special Fields (OpenAcademy)

In your organisation, all the instructions are written on a PDF file. You want
to store this file in your course model, so the instructor can download it. In
your form view, you want to see the corresponding filename, with the possibility
to download the file when you click on it.

We would like to add a price on courses. As an international organisation,
prices come in different currencies. In the form view, the price and currency
should be shown in a nice way: for instance as "$100.00" or "100.00€".

#### Extra Task

Make it possible for a user to change the order of sessions in the course form.


## Problem 3: Improve a Many2many Field (Coop Task Management)

In your model `coopplanning.task.template`, you have a relation with partners:
`worker_ids`. However, it shows in the form view as a list view with name,
phone, email. Improve the view to show a picture for every partner in the
relation.

**Extra Task**

The widget takes too much place. You prefer to have a dropdown widget where you
can select a lot of partners.


## Problem 4: Create a Smart Button (Coop Task Management)

On the model `coopplanning.task.template` we have an active field. You want to
change the value of this field with a special button. Here is the behavior of
this special button:
- if the record is not active,
  - the button label should be "Inactive"
  - on mouse hover, it should change to "Activate"
- if the record is active,
  - the button label should be "Active"
  - on mouse hover, it should change to "Deactivate"

You also want to add a button on the contact form. In this button, you want to
see the number of tasks for this contact. When you click on it, it opens the
list of all the tasks for this partner.


## References

* [Widget in view](https://www.odoo.com/documentation/10.0/reference/views.html)
* [Stat button](http://fr.slideshare.net/openobject/odoo-smart-buttons)
* [Widget list](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/web/static/src/js/views/form_widgets.js#L1680)
