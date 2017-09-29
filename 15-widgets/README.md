# Widgets

## Goals

* interact with module system
* understand widget lifecycle
* be able to create new widgets
* be able to perform various kind of RPCs
* coordinate data fetching and rendering widgets
* adding external libraries (lazyloading/or not)


## Requirements

* [Basic Views](../03-views)
* Basic knowledge of Javascript

## Starting point

* [Library application](./library)

## Problem 1: Fancy Library Dashboard

The library big boss just tried your Library application and he is not pleased.  He got a large amount of public funding to pay for the library application, but clearly, the work you did will not convince the auditors that the money was well spent.

Your task is to improve the current application with a nice looking dashboard.

This dashboard should be the main entry point of the library app (clicking on 'Library' should open the dashboard). The dashboard should have 3 sections (in no particular order)

### Quick navigation

We want a section with various buttons: one button 'Lost books' (open a list view with all rentals lost), one button 'Bad Customers' (open a list view with all customers which owes more than 10$, sorted)

### Statistical informations

We also want another section with various numbers: total amount of money in and out this month, total number of books rented this month, total number of books lost this month

### A fancy pie chart

Finally, everyone likes charts, so let us add a fancy pie chart with the number of books in stock/rented/lost state. (use a JS library not already in odoo)

#### Extra tasks:

- For maximal efficiency, the fancy pie chart JS library should be lazy loaded
- clicking on a section of the fancy pie chart should open a list view of all books, with a filter on the corresponding state (so, lost/returned/rented/....)
- add a control panel to your client action, and put the various buttons from the dashboard in the control panel
- make sure your application can be translated...


## Resources

### References

* [Chart.js](http://www.chartjs.org/)
* Client actions (not really any documentation...)

### Code samples

* [Registering a client action](https://github.com/odoo/odoo/blob/dbf8304e3a7b66a76854170fe1e166d56da72e1a/addons/web_settings_dashboard/static/src/js/dashboard.js#L344)
* [Lazy loading](https://github.com/odoo/odoo/blob/f1a85ba70a2412fb0d7bf789a758d8f2d2e86a02/addons/website/static/src/js/backend/dashboard.js#L49)
* [rpc on a model](https://github.com/odoo/odoo/blob/dbf8304e3a7b66a76854170fe1e166d56da72e1a/addons/website/static/src/js/menu/content.js#L194)
* [rpc on a controller](https://github.com/odoo/odoo/blob/dbf8304e3a7b66a76854170fe1e166d56da72e1a/addons/web/static/src/js/chrome/user_menu.js#L62)