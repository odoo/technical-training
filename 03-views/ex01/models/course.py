# -*- coding: utf-8 -*-
from datetime import timedelta
from openerp import models, fields, api, exceptions, _

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char()
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")
    level = fields.Selection([(1, 'Easy'), (2, 'Medium'), (3, 'Hard')], string="Difficulty Level")
    session_count = fields.Integer("Session Count", compute="_compute_session_count")

    @api.one
    @api.depends('session_ids')
    def _compute_session_count(self):
        self.session_count = len(self.session_ids)


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=lambda self : fields.Date.today())
    end_date = fields.Date(default=lambda self : fields.Date.today())
    active = fields.Boolean(default=True)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one('res.partner', string="Instructor")
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees", domain=[('is_company', '=', False)])
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    level = fields.Selection(related='course_id.level', readonly=True)
    responsible_id = fields.Many2one(related='course_id.responsible_id', readonly=True, store=True)
    description = fields.Html()

    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        if not self.seats:
            self.taken_seats = 0.0
        else:
            self.taken_seats = 100.0 * len(self.attendee_ids) / self.seats

    @api.one
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        self.attendees_count = len(self.attendee_ids)

    @api.onchange('start_date', 'end_date')
    def _compute_duration(self):
        if not (self.start_date and self.end_date):
            return
        if self.end_date < self.start_date:
            return self._warning("Incorrect date value", "End date is earlier then start date")
        delta = fields.Date.from_string(self.end_date) - fields.Date.from_string(self.start_date)
        self.duration = delta.days + 1
