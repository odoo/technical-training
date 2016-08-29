# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Partner(models.Model):
    _name = 'openacademy.partner'

    name = fields.Char('Name',)
    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)


