# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api


def float_to_time(f):
    decimal, integer = math.modf(f)
    return "%s:%s" % (str(int(integer)).zfill(2), str(int(round(decimal * 60))).zfill(2))


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
    end_time = fields.Float()

    duration = fields.Float(compute='_get_duration', help="Duration in Hour", store=True)
    worker_nb = fields.Integer(string="Number of worker", help="Max number of worker for this task", default=1)
    worker_ids = fields.Many2many('res.partner', string="Recurrent worker assigned")
    active = fields.Boolean(default=True)

    @api.depends('start_time', 'end_time')
    def _get_duration(self):
        for rec in self:
            rec.duration = rec.end_time - rec.start_time
