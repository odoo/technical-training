# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=lambda self : fields.Date.today())
    active = fields.Boolean(default=True)
    duration = fields.Float(digits=(6, 2), help="Duration in days", default=1)
    instructor_id = fields.Many2one('openacademy.partner', string="Instructor") 
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('openacademy.partner', string="Attendees")
    state = fields.Selection([
                    ('draft', "Draft"),
                    ('confirmed', "Confirmed"),
                    ('done', "Done"),
                    ], default='draft')
