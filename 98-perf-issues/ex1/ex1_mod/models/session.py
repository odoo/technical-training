# -*- coding: utf-8 -*-
import names
import random

from odoo import models, fields, api, exceptions, _

class Session(models.Model):
    _name = 'openacademy.session'
    _inherit = 'mail.thread'

    name = fields.Char(required=True)
    start_date = fields.Date(default=lambda self : fields.Date.today())
    active = fields.Boolean(default=True)
    duration = fields.Float(digits=(6, 2), help="Duration in days", default=1)
    instructor_id = fields.Many2one('res.users', string="Instructor") 
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.One2many('openacademy.registration', 'session_id', string="Attendees")
    state = fields.Selection([
                    ('draft', "Draft"),
                    ('confirmed', "Confirmed"),
                    ('started', "Started"),
                    ('done', "Done"),
                    ], default='draft')
    session_cost = fields.Float('Cost', compute='_compute_cost')
    course_cost = fields.Float('Course Cost', compute='_compute_cost')
    
    @api.depends('course_id.session_ids.session_cost', 'attendee_ids')
    def _compute_cost(self):
        for rec in self:
            cost = 0
            for att in rec.attendee_ids:
                cost += att.with_context({'default_attendee_id': att.id}).attendee_id.get_cost()
            rec.session_cost = cost
            course_cost = 0
            for sess in rec.course_id.session_ids:
                course_cost += sess.with_context({'default_session_id': sess.id}).session_cost
            rec.course_cost = course_cost
