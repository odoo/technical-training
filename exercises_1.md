![Odoo Logo](https://odoocdn.com/openerp_website/static/src/img/assets/png/odoo_logo_small.png)

# Odoo JS - Module 1 - Widgets

## Content

- [Introduction](#introduction)
- Tasks
    - [1.1 Create empty dashboard](#11-create-empty-dashboard)
    - [1.2 Add a simple widget](#12-add-a-simple-widget)
    - [1.3A Add quick navigation](#13a-add-quick-navigation)
    - [1.3B: Add various statistics](#13b-add-various-statistics)
    - [1.3C Pie chart](#13c-pie-chart)
    - [1.4 Auto updating the dashboard](#14-auto-updating-the-dashboard)
    - [Extra Tasks](#extra-tasks)

## Introduction

Widgets are the basic UI building blocks in Odoo.  They are mostly equivalent
to the notion of *component* in other popular frameworks. Odoo widgets are
defined imperatively.  Creating a sub widget need to be done in javascript.


## 1.1 Create empty dashboard

#### Goals

- work with the odoo JS modules
- add a file to the assets
- create and understand client actions

#### Task Description

Bosses like dashboards. Here is what we would like to do:

- create a new file `awesome_dashboard.js` in `static/src/js` with a simple
  `console.log('hello world')`
- add it to the `assets_backend` bundle
- make sure it is loaded (and you can see the message in the console)
- replace the content of the file with an odoo module (`awesome_tshirt.dashboard`)
- create a new client action and register it
- add a new menu item T-Shirt Dashboard, which opens this client action

This client action is a widget, which we will use to display our custom
dashboard. This dashboard should have 3 parts, which are independant tasks.

#### Resources

* [Assets management](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#assets-management)
* [Odoo Module System](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#javascript-module-system)
* [Adding a client action](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#adding-a-client-action)
* [Client Actions](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#client-actions)


## 1.2 Add a simple widget

#### Goals

- create a widget from scratch
- import your code in another file
- understand how to instantiate a widget and append it to the dom
- understand how to add behaviour (with events/handlers) to a widget

#### Task Description

This is not really in the scenario, but it is useful to see a simple example of
a widget.  For this exercise, we will create a counter widget.

- create a `MyCounter` widget, in its own file, and add it to the dashboard
- this widget should simply render a template with 2 buttons (+ and -) and a
  `span` which display a counter, initially set to 0
- clicking on these buttons should increment/decrement the value

#### Resources

* [Widget API](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#widgets)
* [QWeb Template engine](https://www.odoo.com/documentation/12.0/reference/qweb.html)


## 1.3A Add quick navigation

#### Goals

- use Qweb templates
- add behaviour to a widget
- execute actions from JS
- understand how to create 'dynamic' action (purely in JS)

#### Task Description

This should be a simple div with various buttons:
- a button `Customers`, which opens a kanban view with all customers (this
    action already exists in `xml`)
- a button `New Orders`, which opens a list view with all orders created in
    the last 7 days
- a button `Cancelled Order`, which opens a list of all orders cancelled in
    the last 7 days

#### Resources

* [`do_action` method](https://github.com/odoo/odoo/blob/9393a0eba88cad6184b5255a11f6a5a2996528cc/addons/web/static/src/js/core/service_mixins.js#L187)
* [example of `do_action` use](https://github.com/odoo/odoo/blob/9393a0eba88cad6184b5255a11f6a5a2996528cc/addons/web/static/src/js/tools/debug_manager.js#L285)
* [`res_partner` action](https://github.com/odoo/odoo/blob/a0ff2966b6db4e652fdc19a2f792af8cf3e5ce69/odoo/addons/base/views/res_partner_views.xml#L585)

## 1.3B: Add various statistics

#### Goals

- load data from the server
- use the proper hooks in a widget

#### Task Description

another `div`, with various statistics:
- number of new orders this month
- total amount of new orders this month
- average amount of t-shirt by order this month
- number of cancelled orders this month
- average time for an order to go from 'new' to 'sent' or 'cancelled'

Make sure the widget is only displayed when the data is ready.

Note: the module comes with a controller which returns those statistics. It is
located in the file `main.py`, and will answer to the url
`/awesome_tshirt/statistics`.


#### Resources

* [rpc documentation](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#rpcs)
* [widget lifecycle](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#widget-lifecycle)

## 1.3C Pie chart

#### Goals

- load assets from the server
- integrate an external library
- use and manipulate a widget

#### Task Description

Finally, everyone likes charts, so let us add a pie chart in a last section,
which displays the proportions of t-shirts sold for each size: S/M/L/XL/XXL

For this exercise, we want to use `Chart.js`, add it to the assets (or not?),
create a widget (it is strictly not necessary, but this is an exercise!), and
display the required information


#### Resources

* [ChartJS](http://www.chartjs.org/)
* [ChartJS Pie example](http://www.chartjs.org/samples/latest/charts/pie.html) (inspect page source for the code)
* [Adding file to a bundle](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#adding-files-in-an-asset-bundle)
* [Lazy load assets example](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web_editor/static/src/js/widgets/widgets.js#L1597)

## 1.4 Auto updating the dashboard

#### Goals

- see how new specifications affect existing code
- understand how `on_attach_callback` and `on_detach_callback` are used

#### Task Description

The Awesome Tshirt new manager want to be able to automatically reload the
dashboard periodically, to make sure he is totally up to date.  It was decided
that triggering a reload every 30s was an acceptable solution.

- modify the dashboard to automatically reload itself
- make sure it does not do anything if not visible (check the network tab)

#### Resources

- [`setInterval`](https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/setInterval)
- [Example of `on_attach_callback`, `on_detach_callback`](https://github.com/odoo/odoo/blob/saas-12.5/addons/mail/static/src/js/discuss.js#L334)

## Extra tasks:

#### Goals

- think about the tradeoffs between various way to use/load assets
- add behaviour to external library code
- use the `ControlPanelMixin`
- understand how odoo JS translation system should be used

#### Task Description

- For maximal efficiency, the fancy pie chart JS library should be lazy loaded. If you did not do
  it yet, do it now.
- clicking on a section of the pie chart should open a list view of all orders
  which have the corresponding size,
- add a control panel to your dashboard, and put the various buttons from the
  dashboard in the control panel
- make sure your application can be translated...

#### Resources

- [Control panel mixin doc](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#using-the-control-panel-mixin)
- [Translation system in Odoo](https://www.odoo.com/documentation/12.0/reference/translations.html)
- [Translation in JS documentation](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#translation-management)
