# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Registration(models.Model):
    _name = 'openacademy.registration'
    _inherit = 'mail.thread'
    
    _order_by = 'course_id, session_id'
    
    name = fields.Char(compute='_compute_name', store=True)
    session_id = fields.Many2one('openacademy.session', ondelete='cascade', string="session", required=True)
    course_id = fields.Many2one('openacademy.course', related='session_id.course_id', store=True)
    attendee_id = fields.Many2one('res.partner', string="Attendee")
    
    @api.depends('attendee_id.name', 'session_id.name', 'course_id.name')
    def _compute_name(self):
        for rec in self:
            rec.name = "%s - %s - %s" % (rec.attendee_id.name, rec.session_id.name, rec.course_id.name)
