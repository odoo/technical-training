# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from odoo import models, fields, api, exceptions, _

from pytz import UTC, timezone
import math

def float_to_time(f):
    decimal, integer = math.modf(f)
    return "%s:%s" % (str(int(integer)).zfill(2), str(int(round(decimal * 60))).zfill(2))

def floatime_to_hour_minute(f):
    decimal, integer = math.modf(f)
    return int(integer), int(round(decimal * 60))

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

class Planning(models.Model):
    _name = 'coopplanning.planning'

    name = fields.Char()
    task_template_ids = fields.One2many('coopplanning.task.template', 'planning_id')

    @api.multi
    def open_task_generation_wizard(self):
        self.ensure_one()
        return {
           'name': _('Generate Task'),
           'type': 'ir.actions.act_window',
           'view_type': 'form',
           'view_mode': 'form',
           'res_model': 'coopplanning.instanciate_planning.wizard',
           'target': 'new',
        }

class TaskTemplate(models.Model):
    _name = 'coopplanning.task.template'

    name = fields.Char(required=True)
    planning_id = fields.Many2one('coopplanning.planning', required=True)
    day_nb_id = fields.Many2one('coopplanning.daynumber', string='Day')
    task_type_id = fields.Many2one('coopplanning.task.type', string="Task Type")
    start_time = fields.Float()
    end_time = fields.Float()

    duration = fields.Float(compute='_get_duration', help="Duration in Hour", store=True)
    worker_nb = fields.Integer(string="Number of worker", help="Max number of worker for this task", default=1)
    worker_ids = fields.Many2many('res.partner', string="Recurrent worker assigned")
    active = fields.Boolean(default=True)
    floating = fields.Boolean("Floating Task", help="This task will be not assigned to someone and will be available for non recurring workers")

    @api.multi
    @api.depends('start_time', 'end_time')
    def _get_duration(self):
        for rec in self:
            rec.duration = rec.end_time - rec.start_time

    @api.multi
    def generate_task(self):
        self.ensure_one()
        today = datetime.today()
        self._generate_task_day(today)

    def _generate_task_day(self, today):
        task = self.env['coopplanning.task']
        h_begin, m_begin = floatime_to_hour_minute(self.start_time)
        h_end, m_end = floatime_to_hour_minute(self.end_time)
        for i in xrange(0, self.worker_nb):
            task.create({
                'name' :  "%s (%s) - (%s) [%s]" % (self.name, float_to_time(self.start_time), float_to_time(self.end_time), i),
                'task_template_id' : self.id,
                'task_type_id' : self.task_type_id.id,
                'worker_id' : self.worker_ids[i].id if len(self.worker_ids) > i else False,
                'start_time' : fields.Datetime.context_timestamp(self, today).replace(hour=h_begin, minute=m_begin, second=0).astimezone(UTC),
                'end_time' :  fields.Datetime.context_timestamp(self, today).replace(hour=h_end, minute=m_end, second=0).astimezone(UTC),
            })