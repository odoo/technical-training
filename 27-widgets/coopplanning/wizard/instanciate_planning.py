# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import timedelta
from datetime import datetime


class InstanciatePlanning(models.TransientModel):
    _name = 'coopplanning.instanciate_planning.wizard'

    def _get_planning(self):
        return self._context.get('active_id')

    date_start = fields.Date("First Day of planning", required=True)
    planning_id = fields.Many2one('coopplanning.planning', readonly=True, default=_get_planning)

    @api.multi
    def generate_task(self):
        self.ensure_one()
        date = datetime.strptime(self.date_start, '%Y-%m-%d')
        for task_template in self.planning_id.task_template_ids:
            day = date + timedelta(days=task_template.day_nb_id.number)
            task_template._generate_task_day(day)
