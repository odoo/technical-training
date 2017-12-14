# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char()
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")
    level = fields.Selection([(1, 'Easy'), (2, 'Medium'), (3, 'Hard')], string="Difficulty Level")
    color = fields.Integer()
    session_count = fields.Integer("Session Count", compute="_compute_session_count")

    _sql_constraints = [
       ('name_description_check', 'CHECK(name != description)',
        _("The title of the course should not be the description")),

       ('name_unique', 'UNIQUE(name)',
        _("The course title must be unique")),
    ]

    @api.one
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', _(u"Copy of {}%".format(self.name)))])
        if not copied_count:
            new_name = _(u"Copy of {}").format(self.name)
        else:
            new_name = _(u"Copy of {} ({})").format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    @api.one
    @api.depends('session_ids')
    def _compute_session_count(self):
        self.session_count = len(self.session_ids)

class Session(models.Model):
    _name = 'openacademy.session'

    _order = 'name'

    name = fields.Char(required=True)
    start_date = fields.Date(default=lambda self : fields.Date.today())
    #end_date = fields.Date(default=lambda self : fields.Date.today())
    end_date = fields.Date(string='End date', store=True, compute='_get_end_date', inverse='_set_end_date')
    active = fields.Boolean(default=True)
    duration = fields.Float(digits=(6, 2), help="Duration in days", default=1)
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one('res.partner', string="Instructor") #No ondelete = set null
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.One2many('openacademy.attendee', 'session_id', string="Attendees", )
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    level = fields.Selection(related='course_id.level', readonly=True)
    responsible_id = fields.Many2one(related='course_id.responsible_id', readonly=True, store=True)
    description = fields.Html()

    percentage_per_day = fields.Integer("%", default=100)
    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)
    color = fields.Integer()
    state = fields.Selection([
                    ('draft', "Draft"),
                    ('confirmed', "Confirmed"),
                    ('done', "Done"),
                    ], default='draft')

    def _warning(self, title, message):
            return {
              'warning': {
                'title': title,
                'message': message,
              },
            }

    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        if not self.seats:
            self.taken_seats = 0.0
        else:
            self.taken_seats = 100.0 * self.attendees_count / self.seats

    @api.one
    @api.depends('attendee_ids', 'seats', 'attendee_ids.state')
    def _get_attendees_count(self):
        self.attendees_count = len(self.attendee_ids.filtered(lambda rec: rec.state in ['confirmed', 'done']))

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return self._warning(_("Incorrect 'seats' value"), _("The number of available seats may not be negative"))
        if self.seats < len(self.attendee_ids):
            return self._warning(_("Too many attendees"), _("Increase seats or remove excess attendees"))

    @api.one
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        if self.instructor_id and self.instructor_id in self.attendee_ids.mapped('partner_id'):
            raise exceptions.ValidationError("A session's instructor can't be an attendee")

    @api.one
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        if not (self.start_date and self.duration):
            self.end_date = self.start_date
            return
        # Add duration to start_date, but: Monday + 5 days = Saturday, so
        # subtract one second to get on Friday instead
        start = fields.Datetime.from_string(self.start_date)
        duration = timedelta(days=self.duration, seconds=-1)
        self.end_date = start + duration

    @api.one
    def _set_end_date(self):
        if not (self.start_date and self.end_date):
            return
        # Compute the difference between dates, but: Friday - Monday = 4 days,
        # so add one day to get 5 days instead
        start_date = fields.Datetime.from_string(self.start_date)
        end_date = fields.Datetime.from_string(self.end_date)
        self.duration = (end_date - start_date).days + 1

    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_confirm(self):
        self.state = 'confirmed'

    @api.one
    def action_done(self):
        self.state = 'done'

class Attendee(models.Model):
    _name = 'openacademy.attendee'

    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', 'Attendee Name', domain=[('is_company', '=', False)])
    session_id = fields.Many2one('openacademy.session', 'Session')
    course_id = fields.Many2one('openacademy.course', string="Course")

    state = fields.Selection([
                    ('draft', "Draft"),
                    ('confirmed', "Confirmed"),
                    ('done', "Attended"),
                    ('cancel', "Not Attended"),
                    ], default='draft')

    _sql_constraints = [
       ('subscribe_once_per_session', 'UNIQUE(partner_id, session_id)',
        _("You can only subscribe a partner once to the same session.")),
    ]

    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_confirm(self):
        self.state = 'confirmed'

    @api.one
    def action_done(self):
        self.state = 'done'

    @api.one
    def action_cancel(self):
        self.state = 'cancel'
