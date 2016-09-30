# Mail Integration

## Goal

In this module, you will learn how to integrate your new business model with the
messaging system in Odoo. You will:

* configure incoming and outgoing mail servers;
* understand the alias system and the mechanism of email routing on the catchall address;
* enable the messaging feature to any business model;
* create new records at email reception on a specific alias:
    * define specific default value for aliases,
    * link an alias to a specific record;
* integrate mail notifications based on a template inside a business flow;
* automatically include people in discussions;
* track the changes of a record in its message thread;
* understand how email subtypes work and define new subtypes.

## Requirements

* [Models, Fields and Relations](../01-models)
* [Computed Fields, Onchange and Constraints](../02-fields)


## Problem 1: Enable Discussions inside OpenAcademy

### Part 1: Enable Discussions on Courses

The OpenAcademy module is going well with its new system to manager courses,
sessions and attendees. The attendee model has been improved: it is now a model
distinct from contacts (model `res.partner`) and has its own business logic. An
attendee record has four possible states: draft, confirmed, attended, and not
attended.

The courses are evolving over time, and the responsibles want to discuss about
their course with the teacher. They heard about the Odoo messaging system on the
sale order, and they want this feature on their course model. Of course, the
responsible of a course should be included in all the discussion about the
course. The teachers of the course's sessions should be suggested to be part of
the discussion.

Once a message is posted on a course, an email should reach the given
recipients. When a recipient replies to the email, its response should find its
way to be appended to the course's message thread.

- **Hint**: inheritance of the mixin model `mail.thread` is the key.

### Part 2: Subscribe to a Session by Email

The current subscription process is very old-fashioned: the trainee calls the
academy, and the operator subscribes them directly in the session view or with
the subscription wizard. It is time to enable an automatic subscription by
email.

When a session is created, the responsible of the corresponding course will
choose an email alias for that session. A trainee will be able to subscribe
simply by sending an email to this alias. When processing that email, the
application automatically creates an attendee record in draft state. A manual
operation is necessary to confirm the attendee subscription. It would be
interesting to keep the subject of the sent email somewhere on the attendee
record.

- **Hint**: use inheritance with mixin models `mail.thread` and `mail.alias`.
- **Testing Hint**: some email providers (like Gmail) make it possible to use a
  single email address for multiple aliases; for instance, all messages sent to
  `foo+friends@gmail.com` and `foo+bank@gmail.com` are automatically redirected
  to `foo@gmail.com`.

#### Extra Task

The alias on the session is fine, but trainees may keep subscribing for sessions
that are full or over. Let us improve this situation. The idea is to define an
alias on the course instead of the session. The trainee that sends a email to
the course alias will be automatically subscribed to the nearest confirmed
session with remaining seats. If no such session exists, the attendee will wait
to be linked to a new session.

### Part 3: Automatically Notify the Attendee

With the system we have so far, trainees may complain about the lack of feedback
about their subscription. They don't know whether their email arrived, or when
their subscription is confirmed. In order to address that issue, the system is
going to send email at each step of the subscription process. Be careful: the
trainee should be able to reply to those emails and its reply should find its
way to the attendee message thread.


## Problem 2: Track Changes on Tasks and Task Templates (Cooperative Planning)

We assume that the planning generation works well now. However, the responsible
of the planning is tired of sending emails to all the workers assigned to
confirm on which task they are working. They heard about the notification system
on Odoo projects, and want something similar. When a task is created or
something is changed on a task, a notification should be send to all the
followers of the task. The worker should automatically be added as a follower in
order to receive those notifications.

#### Extra Task

When the worker of a task is modified, a message with a specific subtype should
be sent. All the followers of the task will be subscribed to this subtype by
default.


## Resources

### References

* [Mail Thread](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/mail/models/mail_thread.py)
* [Mail Alias](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/mail/models/mail_alias.py)
* [Mail Template](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/mail/models/mail_template.py)

### Code Samples

* [Sale Order](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/sale/models/sale.py)
* [Task Suggests Recipient](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/project/models/project.py#L640)
* [Mail Alias on Project](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/project/models/project.py#L52)
* [Email Template Example](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/sale/data/mail_template_data.xml)
* [Track Subtypes](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/project/models/project.py#L544)
