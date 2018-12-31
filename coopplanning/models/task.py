# -*- coding: utf-8 -*-
from odoo import fields, models


class TaskType(models.Model):
    _name = 'coopplanning.task.type'
    _description = 'Task Type'

    name = fields.Char()
    description = fields.Text()

    area = fields.Char()
    active = fields.Boolean(default=True)


class TaskTemplate(models.Model):
    _name = 'coopplanning.task.template'
    _description = 'Task Template'

    name = fields.Char(required=True)

    day_nb_id = fields.Many2one('coopplanning.daynumber', string='Day')
    task_type_id = fields.Many2one('coopplanning.task.type', string="Task Type")

    start_time = fields.Float()
    duration = fields.Float(help="Duration in Hour")

    worker_nb = fields.Integer(string="Number of worker", help="Max number of worker for this task", default=1)
    worker_ids = fields.Many2many('coopplanning.partner', string="Recurrent worker assigned")
    active = fields.Boolean(default=True)
