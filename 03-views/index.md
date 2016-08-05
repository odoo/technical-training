# Actions, Menu and Views


## 1. Goal



The goal of this module is to learn how to display information for the end user, to learn how to design basic view and how to alter fields property

* Be able to activate and use the developer mode
* Be able to add new menu item
* Be able to link windows action to menu item
* Be able to design list, form and search views from scratch 
* Be able to design embedded views for Many2many and One2many
* Be able to define field's property, statically and dynamically

## 2. Requirements

* [01. Models](../01-models/)
* [02. Fields](../02-fields/)


## 3. Problem 01: Display course and session for Openacademy


We have design two models course and session, we have define some fields on them but when we install the module nothing change in odoo UI. It's time to change that. 
We will have more then one course and more. This mean we need to show the a list of all the course and show a list of all the session. The user has to be able to see the detail of each course and each session in a separate form. 

Of course, those feature should be available directly once the module is installed. 


- **directory** : 03-views/ex01
- **Technical Hint**: Explore developer mode. Check for tree views and form views. Check for windows actions and menu Items

#### Extra task


* We want to display a nice Icon for the top menu of the Openacademy application in the app switcher. 
* The percentage of seats taken could be display with a more visual widget like a progressbar

## 4. Problem 02: search and order task in Coop Task Management

The planning template is a list of task template. A task template has a type, a start time, an end time, a duration, a day number, a duration, a number of worker and a list of predefined worker. There is also a active field that allow to archive them. it's possible to search on all those field but only with the advance search. Only the name can be search directly.

We would like to be able to quick search on the task type, on the day number and on the predefined worker. We would like also to easily switch from active template to archived ones.
For the task type and the day number,we want to able to find task templates based on the name of the task type but also the area, respectively the number for day number.


- **directory** : 03-views/ex02
- **Technical Hint**: This a new type of view the search view, related field could be handy or you can explore the name_search


#### Extra task

* It could be interesting to have a quick way to see all the task template (active and archived ones). 
* It would be easier to visualize the planning if the task template are sorted by Day number then by Start time.








## 5. Problem 03: Improve Form Views in Coop Task Management


We are still working on the planning management use case.
A new model task has been add, it's tree and form view as well. The record of this model are instances of a task template. It represent someone working on a specific task type at a specific time and date. A button generate task has been added on the task template. This button generate has much task has the worker number assign pre assign worker on those task adn set the time. The button is not smart enough to take care of the day number so the task are created for today. 

We would like to improve a bit the user experience. First on the task form, if the task is created from a task template, the user should not be able to change the task template field and the task type on that task. If the task is directly created from the menu task, the field task template should not be visible. 

We do not want to have user that create by mistake Day Number and Task Template on the Task and Task Template form. 

A new field on the task template has been added "Floating", it means the task template is dedicated for worker that cannot subscribe for a recurring task, in other words no pre assigned workers should be set on those template. If the the Task Template has the box "Floating" ticked, the user should not be able to assigned any worker on this template.

The fields Pre defined Worker, show a list of workes name, phone and email. We would like to show more information, for example the language of the worker and the tags linked to him, in this list and only in this list.

Users should not be able to create Task Template without task type and Day Number or a Task without a Task Type

Finally, the field start_time, end_time and duration represent time which are usually express in 60 base and not in 10 based number (7:30 instead of 7.5), It would be great to show the data in that format.

- **directory** : 03-views/ex03
- **Technical Hint**:  Everything can be done in the views. Domain can be handy. 

#### Extra task
* Since it's not possible to create Task Template and Day Number from the other object, we will need a configuration menu to be able to create and edit those object.
* Make sure the menu are always in the same order in any circumstance




-------------------------------------



## 6. Resources


### Reference

* [Activate Debug Mode](https://www.odoo.com/documentation/9.0/howtos/web.html#a-simple-module)
* [Data Files Documentation](http://www.odoo.com/documentation/9.0/reference/data.html)
* [DOC] on menu ITEM : TODO
* [Action Documentation](http://www.odoo.com/documentation/9.0/reference/actions.html)
* [Views Documentation](http://www.odoo.com/documentation/9.0/reference/views.html)
* [Fields Documentation](http://www.odoo.com/documentation/9.0/reference/orm.html#basic-fields)
* [Online Tutorial](http://www.odoo.com/documentation/9.0/howtos/backend.html#basic-views)
* [Domains](https://www.odoo.com/documentation/9.0/reference/orm.html#domains)


### Code Sample

* [Odoo Views Example](https://github.com/odoo/odoo/blob/9.0/addons/product/product_view.xml)
* [Odoo MenuItem Example](https://github.com/odoo/odoo/blob/9.0/addons/account/views/account_menuitem.xml)
* [Odoo Example of module fancy description](https://github.com/odoo/odoo/tree/9.0/addons/account/static/description)
* [CRM tree view ordered](https://github.com/odoo/odoo/blob/9.0/addons/crm/crm_lead_view.xml#L661)
* [Attrs](https://github.com/odoo/odoo/blob/9.0/addons/hr_recruitment/views/hr_recruitment_views.xml#L416)
* [Use of Options in Views](https://github.com/odoo/odoo/blob/9.0/addons/hr_recruitment/views/hr_recruitment_views.xml#L411)








