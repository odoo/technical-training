# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class Partner(models.Model):
    _inherit = 'res.partner'

    task_count = fields.Integer('N° task', compute='_number_task')

    def _number_task(self):
        for partner in self:
            partner.task_count = self.env['coopplanning.task'].search_count([('worker_id', '=', partner.id)])

    def task_button(self):
        self.ensure_one()
        task_ids = self.env['coopplanning.task'].search([('worker_id', '=', self.id)])

        return {
            'name': 'Partner Task',
            'view_mode': 'tree, form',
            'res_model': 'coopplanning.task',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'domain': [('id', 'in', task_ids.ids)],
        }
