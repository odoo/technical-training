# -*- coding: utf-8 -*-
import math
from datetime import datetime
from pytz import UTC

from odoo import api, fields, models


def float_to_time(f):
    decimal, integer = math.modf(f)
    return "%s:%s" % (str(int(integer)).zfill(2), str(int(round(decimal * 60))).zfill(2))


def floatime_to_hour_minute(f):
    decimal, integer = math.modf(f)
    return int(integer), int(round(decimal * 60))


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
    day_nb = fields.Integer(related='day_nb_id.number', string='Day Number')
    task_type_id = fields.Many2one('coopplanning.task.type', string="Task Type")

    start_time = fields.Float()
    duration = fields.Float(compute='_compute_duration', help="Duration in Hour", store=True)
    end_time = fields.Float()

    worker_nb = fields.Integer(string="Number of worker", help="Max number of worker for this task", default=1)
    worker_ids = fields.Many2many('res.partner', string="Recurrent worker assigned")
    active = fields.Boolean(default=True)

    task_area = fields.Char(related='task_type_id.area', string='Task Area')
    floating = fields.Boolean("Floating Task", help="This task will be not assigned to someone and will be available for non recurring workers")

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for rec in self:
            rec.duration = rec.end_time - rec.start_time

    def generate_task(self):
        self.ensure_one()
        task = self.env['coopplanning.task']
        today = datetime.today()
        h_begin, m_begin = floatime_to_hour_minute(self.start_time)
        h_end, m_end = floatime_to_hour_minute(self.end_time)
        for i in range(0, self.worker_nb):
            task.create({
                'name':             "%s (%s) - (%s) [%s]" % (self.name, float_to_time(self.start_time), float_to_time(self.end_time), i),
                'task_template_id': self.id,
                'task_type_id':     self.task_type_id.id,
                'worker_id':        self.worker_ids[i].id if len(self.worker_ids) > i else False,
                'start_time':       fields.Datetime.to_string(fields.Datetime.context_timestamp(self, today).replace(hour=h_begin, minute=m_begin, second=0).astimezone(UTC)),
                'end_time':         fields.Datetime.to_string(fields.Datetime.context_timestamp(self, today).replace(hour=h_end, minute=m_end, second=0).astimezone(UTC)),
            })

    @api.onchange('floating')
    def _onchange_floating(self):
        if self.floating:
            self.worker_ids = self.env['res.partner']


class Task(models.Model):
    _name = 'coopplanning.task'
    _description = 'Task'

    name = fields.Char()

    task_template_id = fields.Many2one('coopplanning.task.template')
    task_type_id = fields.Many2one('coopplanning.task.type', string="Task Type")

    start_time = fields.Datetime()
    end_time = fields.Datetime()

    worker_id = fields.Many2one('res.partner')
