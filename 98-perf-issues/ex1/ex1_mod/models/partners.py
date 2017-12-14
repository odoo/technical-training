# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Partner(models.Model):
    _inherit = 'res.partner'
    
    registration_ids = fields.One2many('openacademy.registration', 'attendee_id')

    @api.multi
    def get_cost(self):
        return 42
        
