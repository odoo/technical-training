
# Odoo 12.0 JS Framework - Module 2

## Advanced Customization with JS

Note that this module is mostly independant of module 1.
The basic infrastructure is exactly the same, and it does not require the
completion of the previous exercises.


## Task 2.1A: T-shirt preview widget

Goals:
------
- understand how to create/manipulate a field widget, in edit and in readonly
  mode
- understand how to register a widget to the field registry

Description:
------------
Each new order on the website will be created as an awesome_tshirt.order.  This
model has a image_url field (of type char), which is currently only visible as a
string. We want to be able to see it in the form view.

For this task, we need to create a new field widget 'image_preview'.  This
widget is specified as follows:
- in readonly mode, it is an image tag with the correct src if field is set
- in edit mode, it behaves like classical char fields

Resources:
----------
* [Creating a new field widget](https://www.odoo.com/documentation/12.0/reference/javascript_cheatsheet.html#creating-a-new-field-widget)
* [AbstractField documentation](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#abstractfield)
* [AbstractField code](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/fields/abstract_field.js)
* [Example of a new field widget](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/website/static/src/js/backend/button.js)
* [Field registry](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/fields/field_registry.js)


## Task 2.1B: T-shirt preview widget

Goals:
------
- better understanding of FieldWidget

Description:
------------
We want to improve the widget of the previous task to help the staff recognize
orders for which some action should be done. In particular, we want to display,
in readonly, a warning 'MISSING TSHIRT DESIGN' in red, if there is no image url
specified on the order.

Resources:
----------
* [AbstractField documentation](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#abstractfield)
* [AbstractField code](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/fields/abstract_field.js)
* [isSet function of AbstractField](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/fields/abstract_field.js#L276)


## Task 2.2: isLate widget in form/kanban views

Goals:
------
- extend and modify an existing field widget

Description:
------------
There is a 'is_late', readonly, boolean field on the task model.  This would be
useful to display in the list/kanban/form view.  Make a new field widget
(inheriting from FieldBoolean), which displays a red/green circle, depending if
the boolean is true/false.  Also, add it in the list/kanban/form views of orders.

Bonus point: add options to configure the colors of the widget

Resources:
----------
- [Modifying an existing field widget](https://www.odoo.com/documentation/12.0/reference/javascript_cheatsheet.html#modifying-an-existing-field-widget)
- [Example of a sub field widget, with options](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/fields/basic_fields.js#L923)


## Task 2.3: message for some customers

Goals:
------
- use the form widget API (widget tag)

Description:
------------
For a super efficient workflow, we would like to display a message/warning box
with some information in the form view, with specific messages depending on
some conditions:
- if the image_url field is not set, it should display "No image"
- if the amount of the order is higher than 100 euros, it should display
    "Add promotional material"
Make sure that your widget is updated in real time.

Note: extra challenge for this task: the feature is not documented.

Resources:
----------
- [Example of form widget use](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/tests/views/form_tests.js#L6583)


## Task 2.4: add buttons in control panel

Goals:
------
- be able to customize a form view (sub form view)
- be able to work with various AbstractController methods
- add buttons to a control panel in a view
- add behaviour to these buttons
- change its look depending on some business logic

Description:
------------

### Customer Geolocation

We have big plans for the future, and these plans involves collecting more data
on our customers.  A first step is to make sure we have their GPS coordinates.
(note: this task will also be useful for the module 3)

- add base_geolocalize as a dependency to your module
- in the customer form view, add a button in the control panel to
  geolocalize him (note: it already exists in the notebook)

Note that we only want to do that in the specific form view for customers.

### Print Label

In practice, once the t-shirt order is printed, we need to print a label to put
on the package.  To help with that, let us add a button in the order form view
control panel:

- clicking on this button should call the method print_label from the model
  awesome_tshirt.order, with the proper id (note: print_label is a mock method,
  it only display a message in the logs)
- it should be disabled if the current order is in 'create' mode (i.e., it does
  not exist yet)
- it should be displayed as a primary button if the customer is properly set and
  if the task stage is 'printed'. Otherwise, it is only displayed as a secondary
  button.

Ensure that the button is updated according to the mode of the FormView and to
the record's values.

Bonus point: clicking twice on the button should not trigger 2 rpcs

Resources:
----------
- [Customizing an existing view](https://www.odoo.com/documentation/12.0/reference/javascript_cheatsheet.html#customizing-an-existing-view)
- [renderButtons method](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/chrome/abstract_action.js#L73)
- [renderButtons method example](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/views/form/form_controller.js#L126)
- [\_updateButtons method](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/views/form/form_controller.js#L391)
- [debounce function](https://underscorejs.org/#debounce)


## Task 2.5: Notifications

Goals:
------
- be able to use the notification API

Description:
------------
Note: this task depends on the 'Print Label' subtask for task 4.

After using the 'Print Label' for some t-shirt tasks, it is apparent that there
should be some feedback that the print_label action is completed (or failed,
for example, the printer is not connected or ran out of paper).  Let us
display a notification message when the action is completed succesfully, and a
warning if it failed (and in that case, the notification should be permanent)

Resources:
----------
- [Notification API](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#notifications)


## Task 2.6: add a systray item

Goals:
------
- be able to use the Systray API

Description:
------------
Sometimes, the staff needs to quickly access an order, based on its id (for
example, a customer calls and wants to change some part of its order).  In that
case, an extra quick access to that order is really useful.  Here is what we
want to do:

- create a widget 'QuickOrderNavigation' and add it to the systray
- this widget should have an input
- whenever the user enters an id and press enter, it should open in a new
  action (target=new) a form view with the specific order


Resources:
----------
- [Systray Documentation](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#systray)
- [Example of a Systray item](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/mail/static/src/js/systray/systray_activity_menu.js#L146)


## Task 2.7.1: Customized message in Home screen

Goals:
------
- understand the process of customizing any existing component
- use the .include (monkey patching) method
- understand the component tree

Description:
------------
Your boss, Bafien Ckinpaers, would like to be able to customize the home screen
to add a message to 'encourage' all its employees.

Modify the home menu to add a div with a static message:
"Bafien Ckinpaers is watching you!"

Note: this exercise is enterprise only. If you use the community version, add
the message in the navbar instead.

Resources:
----------
- [Modifying a main widget](https://www.odoo.com/documentation/12.0/reference/javascript_cheatsheet.html#modifying-a-main-widget-from-the-interface)
- [Monkey patching mechanism](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#patching-an-existing-class)
- [Home menu code](https://github.com/odoo/enterprise/blob/d0edbf347ba1ccadbadbabaef7d2e2ff99e8cf40/web_enterprise/static/src/js/home_menu.js)



## Task 2.7.2: Load data from the server

Goals:
------
- understand various methods of getting data to the web client
- load data by calling the server in the proper hook
- add data to session info, to prevent extra rpc

Description:
------------
Of course, Bafien Ckinpaers is not happy with a static message. He wants to be
able to customize it.  For this task, let us assume that there is the proper
infrastructure in place to allow him to edit some record on the database, and
that the message is available as a controller, */awesome_tshirt/bafienistalkingtoyou*.

- load the data in the home menu widget (which hook should be used?) and
  display it instead of the static message as before
- think about the effect of doing one extra rpc. Is it good? is it efficient?
- try an alternate solution: add directly data in the session info
- see what the difference between those two solutions is


Note: home screen is Enterprise only.  If you use community, put the message in
the navbar instead.

Resources:
----------
- [Adding info to the session](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#adding-information-to-the-session)


## Task 2.8: Custom Kanban View (hard)

Goals:
------
- create view specialization
- deeper understanding the architecture MVC of views
- coordinate renderer/controller and sub widgets


Description:
------------

Bafien had the greatest idea ever (after the freeze!): a mix of a Kanban View
and a list widget would be perfect for your needs!  In a nutshell, he wants a
list of customers on the left of the task kanban view.  When you click on a
customer on the left, the kanban view on the right is filtered to only display
orders linked to that customer.

- create a sub kanban view and use it in your action
- in your KanbanController, do a rpc to fetch the list of all customers which
  have an active (not yet sent nor cancelled) order
- display the customers in a list on the left of the kanban view
- when you click on a customer on the CustomerList, it should be displayed as
  selected (maybe change the background), and the kanban view should be filtered
  accordingly.

Hint: there is a 'has_active_order' field on res.partner.

Bonus: add a searchbox in the top of the Customerlist widget to allow the user
to filter on the customer name (note: we have a fuzzy search library
somewhere...).

Resources:
----------
- [Views MVC architecture](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#views)
- [Customizing an existing view](https://www.odoo.com/documentation/12.0/reference/javascript_cheatsheet.html#customizing-an-existing-view)
- [Sub Kanban view example (enterprise)](https://github.com/odoo/enterprise/blob/d0edbf347ba1ccadbadbabaef7d2e2ff99e8cf40/documents/static/src/js/documents_kanban_view.js)

