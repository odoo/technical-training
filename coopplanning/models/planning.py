# -*- coding: utf-8 -*-

from odoo import models, fields


class TaskType(models.Model):
    _name = 'coopplanning.task.type'

    name = fields.Char()
    description = fields.Text()
    area = fields.Char()
    active = fields.Boolean(default=True)


class DayNumber(models.Model):
    _name = 'coopplanning.daynumber'

    name = fields.Char()
    number = fields.Integer("Day Number", help="From 1 to N, When you will instanciate your planning, Day 1 will be the start date of the instance, Day 2 the second, etc...")
    active = fields.Boolean(default=True)


class TaskTemplate(models.Model):
    _name = 'coopplanning.task.template'

    name = fields.Char(required=True)
    day_nb_id = fields.Many2one('coopplanning.daynumber', string='Day')
    task_type_id = fields.Many2one('coopplanning.task.type', string="Task Type")
    start_time = fields.Float()

    duration = fields.Float(string='Duration', help="Duration in Hour")
    worker_nb = fields.Integer(string="Number of worker", help="Max number of worker for this task", default=1)
    worker_ids = fields.Many2many('coopplanning.partner', string="Recurrent worker assigned")
    active = fields.Boolean(default=True)


class Partner(models.Model):
    _name = 'coopplanning.partner'

    name = fields.Char(required=True)
