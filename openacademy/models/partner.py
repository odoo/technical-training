# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add new fields to the res.partner model
    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)
