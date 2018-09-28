# Odoo 12.0 JS Framework - Module 4

## Testing your frontend code

The theme of this training module is to understand and experiment with the
various methods of testing UI code.

UI can be tested.  It is usually not critical, but without tests, we cannot have
the certainty that our users can accomplish their daily tasks properly.  Also,
another benefits is that testing can prevent the introduction of 'regression'.
(for exemple, a bug fix may, or may not, break some other parts of the code).

There are many many different kind of methods/methodologies for testings, with
various benefits.  At Odoo, for our frontend code, we focus mainly on two kinds
of tests:
- integration tests: these tests spawn a real browser which simulates various
  user interactions, such as clicks/entering values in an input.  The goal is
  to check that a 'business' flow can actually be completed, from start to
  finish.  These tests actually run the full stack: database, server and JS
  code should properly coordinate together.
- unit tests: these tests are focused on a small component, isolated from the
  rest of the system.  The goal is to be able to have small/focused tests on a
  single feature, which validate that it works.  They are usually cheap and
  fast.  Also, when they fail, it is usually faster to see where the problem is,
  since the tested code is small.

Notes:
- usually, depending on the kind of code we are talking about, it is better to
  write the test before/at the same time as the code being tested
- most of these exercises are dependant on previous tasks in modules 1, 2 and 3


## Task 4.1: Testing a widget

Goals:
------
- be able to run the qunit test suite
- use qunitjs to write a small simple test

Description:
------------
- add a file my_counter_test.js in static/tests/, with only a console.log inside
- add it to the test bundle
- load the url /web/tests, and check that your console.log statement actually
  works
- add the counter widget file to the test bundle
- add a simple test which does nothing, and check that the test suite picks it up
- fill the test to make sure the widget behaves as expected: displays 0 at start,
  then 2 when the user clicks twice on the + button, then 1 when the user clicks
  once on the - button.
- check that your test pass (and fails if you comment some line in the counter
  widget)

Resources:
----------
- [some documentation on testing](https://www.odoo.com/documentation/12.0/reference/testing.html#testing-js-code)
- [Example of simple test suite](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/tests/chrome/pager_tests.js)


## Task 4.2: Testing a view

Goals:
------
- unit test a view
- use the testutils.createView helper
- mock rpcs

Description:
------------
One of your important work is the extension of the kanban view (from module 2).
This is clearly very important, and may break if Odoo decides to change the view
API. So, we would like a few tests to see if the following features still works:

- kanban extension can be instantiated
- it performs a search_read on all customers
- it displays the results in a list on the left
- filtering customers does not do any rpc
- clicking on a customer filters orders in kanban view

Resources:
----------
- [Test Utils](https://github.com/odoo/odoo/blob/c3048b14657364afbeda31dd852f103b596dc5c7/addons/web/static/tests/helpers/test_utils.js)
- [Mock Server](https://github.com/odoo/odoo/blob/c3048b14657364afbeda31dd852f103b596dc5c7/addons/web/static/tests/helpers/mock_server.js)


## Problem 4.3: write a tour

Goals:
------
- be able to write an integration test (tour in odoo terminology)

Description:
------------
Unit tests only help testing that the JS code works properly, in isolation.
However, we need some assurance that even if the server code changes, our
application will not break.  To do that, we can write a tour.  The tour should
follow these steps:

- start in the home menu
- open the dashboard
- click on a button in the control panel
- come back to the menu
- open the kanban view for tshirt order

Resources:
----------
- [Example of a tour](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/project/static/src/js/tour.js)


## Problem 4.4: test your dashboard

Goals:
------
- familiarize yourself more with the inner workings of the test system

Description:
------------
Testing widgets and views are reasonably simple, with the test utility functions (test_utils.js).  However, it is slightly more difficult to test a widget such as the  dashboard, since it is a client action, and it needs to perform a rpc.

But, there is a useful piece to help mocking RPCs: the mock server.  Write a test for your dashboard.  Your test should:

- instantiate the dashboard and append it to the DOM
- mock the rpc
- make sure the result is properly rendered
- click on one of the navigation button
- make sure a do_action event is triggered
