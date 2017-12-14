# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Task(models.Model):
    _name = 'coopplanning.task'

    name = fields.Char()
    task_template_id = fields.Many2one('coopplanning.task.template')
    task_type_id = fields.Many2one('coopplanning.task.type', string="Task Type")
    worker_id = fields.Many2one('res.partner')
    start_time = fields.Datetime()
    end_time = fields.Datetime()




