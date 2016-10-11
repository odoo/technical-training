# Actions, Menus and Views

## Goal

The goal of this module is to learn how to display information for the end
users, to learn how to design basic views and how to alter field properties.

* Be able to activate and use the developer mode.
* Be able to create a menu item.
* Be able to link windows action to menu item.
* Be able to design list, form and search views from scratch.
* Be able to design embedded views for Many2many and One2many fields.
* Be able to define field properties, statically and dynamically.


## Requirements

* [01. Models, Fields and Relations](../01-models/)
* [02. Computed Fields, Onchange and Constraints](../02-fields/)


## Problem 1: Display Course and Session (OpenAcademy)

We have designed two models Course and Session, we have defined some fields on
them but when we install the module, nothing changes in the Odoo user interface.
It's time to change that.

We will have several courses. This means we need to show a list of all courses,
and a list of all sessions. The user should see the details of each course and
each session in a separate form.

Of course, those features should be available directly once the module is
installed.

- **Technical Hint**: Explore the developer mode. Check for tree views and form
  views. Check for window actions and menu items.

#### Extra Task

* Add a nice icon for the top menu of the Openacademy application in the app switcher.
* Show the percentage of taken seats as a progressbar.


## Problem 2: Search and Order Task in Coop Task Management

The planning template is a list of task templates. A task template has a type, a
start time, an end time, a duration, a day number, a number of workers and a
list of predefined workers. There is also an active field that allows to archive
them. It is possible to search on all those fields, but only with the advanced
search. Only the name can be searched directly.

We would like to search on the task type, on the day number and on the
predefined worker. We would also like to easily switch from active templates to
archived ones.

For the task type and the day number, we want to able to find task templates
based on the name of the task type but also the area, respectively the number
for day number.

- **Technical Hint**: Look at search views. Related fields could be handy, or
  you can explore the method `name_search`.

#### Extra Task

* It could be interesting to see in an easy way all the task templates (active
  and archived ones).
* It would be easier to visualize the planning if the task templates are sorted
  by day number then by start time.


## Problem 3: Improve Form Views in Coop Task Management

We are still working on the planning management use case. A new task model has
been added, together with its tree and form views. The records of this model are
instances of a task template. It represents someone working on a specific task
type at a specific time and date. A button "Generate Task" has been added on the
task template. This button generates as many tasks as workers, assign
preassigned workers on those tasks and set the time. The button is not smart
enough to take care of the day number so the tasks are created for today.

We would like to improve a bit the user experience. First on the task form, if
the task is created from a task template, the user should not be able to change
the fields "Task Template" and "Task Type" on that task. If the task is created
directly from the menu, the field "Task Template" should not be visible.

We want to avoid a user creating by mistake "Day Number" and "Task Template" on
the task and task template form.

We add a new field on the task template: "Floating". It means that the task
template is dedicated for a worker that cannot subscribe for a recurring task.
In other words, no preassigned worker should be set on those templates. If the
the task template has the box "Floating" ticked, the user should not be able to
assign any worker on this template.

The field "Preassigned Workers" shows a list of worker names, phones and emails.
We would like to show more information, for example the language of the worker,
and the tags linked to them, in this list and only in this list.

Users should not be able to create a task template without task type and day
number, or a task without a task type.

Finally, the fields `start_time`, `end_time` and `duration` represent times
which are usually expressed in hours, but shown as 7:30 instead of 7.5. It would
be great to show the data in that format.

- **Technical Hint**:  Everything can be done in the views. Domains can be handy. 

#### Extra Task

* Since it is not possible to create a task template and day number from the
  other object, we need a configuration menu to be able to create and edit those
  objects.
* Make sure the menus are always in the same order in any circumstance.


## Resources

### Reference

* [Activate Debug Mode](https://www.odoo.com/documentation/10.0/howtos/web.html#a-simple-module)
* [Data Files](http://www.odoo.com/documentation/10.0/reference/data.html)
* [DOC] on menu ITEM : TODO
* [Action](http://www.odoo.com/documentation/10.0/reference/actions.html)
* [Views](http://www.odoo.com/documentation/10.0/reference/views.html)
* [Fields](http://www.odoo.com/documentation/10.0/reference/orm.html#basic-fields)
* [Online Tutorial](http://www.odoo.com/documentation/10.0/howtos/backend.html#basic-views)
* [Domains](https://www.odoo.com/documentation/10.0/reference/orm.html#domains)

### Code Samples

* [Views](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/product/views/product_views.xml)
* [Menu Item](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/account/views/account_menuitem.xml)
* [Example of a fancy module description](https://github.com/odoo/odoo/tree/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/account/static/description)
* [CRM tree view ordered](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/crm/views/crm_lead_views.xml#L540)
* [Attrs](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/hr_recruitment/views/hr_recruitment_views.xml#L412)
* [Use of Options in Views](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/hr_recruitment/views/hr_recruitment_views.xml#L102)
