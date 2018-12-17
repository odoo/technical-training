# -*- coding: utf-8 -*-
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    task_count = fields.Integer('N° task', compute='_number_task')
    task_ids = fields.One2many('coopplanning.task', 'worker_id', string='Tasks')
