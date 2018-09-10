# Odoo 12.0 - Technical Training
=======
# Module 18: Testing Your Interface

## Goals

* be able to write unit tests in odoo
* create a simple tour
* understand how to mock RPC

## Requirements

- [Widgets](https://github.com/odoo/technical-training/tree/12.0-15-widgets)
- [Advanced Customization](https://github.com/odoo/technical-training/tree/12.0-16-advanced-customization)

## Problem 1: Testing a widget

It may not be sexy, but testing is important in a very unstable world (such as Odoo Javascript). You are lucky, the library manager understands this and gave you some time to make sure that your addon will keep working.

Write a test to make sure the boolean widget is_late still works.

## Problem 2: Testing a widget with more elaborate rpc

One of your important work is the extension of the kanban view (from previous module). This is clearly very important, and may break if Odoo decides to change the view API. So, we would like a few tests to see if the following features still works:

- kanban extension can be instantiated
- it performs a search_read on all customers
- it displays the results in a list on the left
- filtering customers does not do any rpc
- but it still filters rentals in kanban view

## Problem 3: write a tour

Unit tests only help testing that the JS code works properly, in isolation.  However, we need some assurance that even if the server code changes, our application will not break.  To do that, we can write a tour.  The tour should follow these steps:

- start in the dashboard
- click on menu to open rentals
- create a rental
- confirm it
- go to the customer form view
- return the book

## Problem 4: test your dashboard

Testing widgets and views are reasonably simple, with the test utility functions (test_utils.js).  However, it is slightly more difficult to test a widget such as the library dashboard, since it is a client action, and it needs to perform a rpc.

But, there is a useful piece to help mocking RPCs: the mock server.  Write a test for your dashboard.  Your test should:

- instantiate the dashboard and append it to the DOM
- mock the rpc
- make sure the result is properly rendered
- click on one of the navigation button
- make sure a do_action event is triggered

## Resources

### References

* [Test Utils](https://github.com/odoo/odoo/blob/c3048b14657364afbeda31dd852f103b596dc5c7/addons/web/static/tests/helpers/test_utils.js)
* [Mock Server](https://github.com/odoo/odoo/blob/c3048b14657364afbeda31dd852f103b596dc5c7/addons/web/static/tests/helpers/mock_server.js)


### Code samples

* [Widget test in list view](https://github.com/odoo/odoo/blob/c3048b14657364afbeda31dd852f103b596dc5c7/addons/web/static/tests/fields/basic_fields_tests.js#L378)
* [Testing client actions](https://github.com/odoo/odoo/blob/c3048b14657364afbeda31dd852f103b596dc5c7/addons/account/static/tests/reconciliation_tests.js#L516)
