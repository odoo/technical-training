
# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Course(models.Model):
    _name = 'openacademy.course'
    _inherit = 'mail.thread'
    
    name = fields.Char(name='Title', required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', string="Responsible")
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")
    level = fields.Selection([('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], string="Difficulty Level")
    plannified_days = fields.Integer(compute='_compute_plannified')
    forecasted_days = fields.Integer(compute='_compute_plannified')
    
    @api.depends('session_ids.state')
    def _compute_plannified(self):
        for rec in self:
            rec.plannified_days = sum(self.env['openacademy.session'].search([('course_id', '=', rec.id), ('state', 'in', ['confirmed', 'started'])]).mapped('duration'))
            rec.forecasted_days = sum(self.env['openacademy.session'].search([('course_id', '=', rec.id), ('state', 'in', ['draft',])]).mapped('duration'))
    
