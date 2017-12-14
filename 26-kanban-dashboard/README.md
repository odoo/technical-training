# Kanban Views and Dashboards

## Goal

The goal of this module is to learn how to improve the user experience by using
kanban views and dashboards.

## Requirements

- [Basic Views](../03-views)
- [View Inheritance](../04-view-inheritance)


## Problem 1: Show Courses and Sessions in Kanban Views (OpenAcademy)

Currently, all courses and sessions are displayed using basic views, but we want
to give our users more information at first sight. In order to accomplish this,
we will create different kanban views.

First, create a kind of dashboard (kanban view with ungrouped records) for
managing courses. It will show the following information about the course:
* its name,
* its themes,
* a picture of its responsible user, and
* a link to open its sessions (showing the number of sessions.)

Second, create a kanban view to display sessions. Session records are more
complex than those created for the courses. By default, records must be grouped
by the course they belong to. Also, we want to be able, via a dropdown menu, to
edit session details and to delete a session. It will show the following
information about the session:
* its name,
* a progress bar for taken seats,
* its start and end date (only shown for not done sessions), colored in red when
the date is past, and
* a picture of its instructor.

#### Extra task

* Modify, as you need, the first part (kanban course view), in order to open a
course's sessions in a kanban view grouped by session state.
* Add a link to open its attendees list (showing the number of attendees).
* Make the progress bar able to modify the number of seats from the kanban view
directly.
* Modify the display of attendees inside the session form view, to display it as
a kanban view.

- **Hint**: To make the last task work correctly, you will need to add an HTML
element to allow removing attendees.


## Problem 2: Let Attendees Provide Feedback on Sessions (OpenAcademy)

Odoo offers the possibility for external users to log into the system in order
to follow-up objects of their interest, and also to interact with the system as
needed. Everything related to this feature is already set up inside the module.

We want to allow session attendees to give their feedback about a session they
attended (in state `done`), using a dashboard.

In order to accomplish this, there is a model `openacademy.feedback`
that links a course session with an attendee and the given feedback. Attendees
can only give their feedback once per session. This fact is enforced by an SQL
constraint on the model, but needs to be reflected also in the user interface.

Also, while the model doesn't requires to fulfill the feedback, we don't want to
allow sending empty feedback.


## Resources

### References

* [Kanban view](http://www.odoo.com/documentation/10.0/reference/views.html#kanban)
* [Odoo's JS framework](https://www.odoo.com/documentation/10.0/reference/javascript.html#web-client)
* [Odoo's widgets 101](https://www.odoo.com/documentation/10.0/howtos/web.html#widgets-basics)
* [Odoo's JS Qweb engine](https://www.odoo.com/documentation/10.0/howtos/web.html#the-qweb-template-engine)
* [Communication with the server](https://www.odoo.com/documentation/10.0/howtos/web.html#communication-with-the-odoo-server)
* [Odoo's widget development ](https://www.odoo.com/documentation/10.0/reference/javascript.html#widgets)


### Code Samples

* [Kanban picture](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/odoo/addons/base/res/res_partner_view.xml#L378)
* [Progress bar widget](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/hr_holidays/views/hr_views.xml#L48)
* [Warning color on field](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/hr_recruitment/views/hr_recruitment_views.xml#L276)
* [Editable progress bar widget](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/hr_recruitment/views/hr_job_views.xml#L68)
* [X2Many field as kanban view](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/odoo/addons/base/res/res_partner_view.xml#L201)
