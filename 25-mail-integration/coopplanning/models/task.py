# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Task(models.Model):
    _name = 'coopplanning.task'

    #EX01 ADD inheritance
    _inherit = ['mail.thread']

    #EX01 Change track visibility
    name = fields.Char(track_visibility='always')
    task_template_id = fields.Many2one('coopplanning.task.template')
    task_type_id = fields.Many2one('coopplanning.task.type', string="Task Type")
    worker_id = fields.Many2one('res.partner', track_visibility='onchange')
    start_time = fields.Datetime(track_visibility='always')
    end_time = fields.Datetime(track_visibility='always')

    #Ex01: hook the add follower before the creation of mail.message
    def message_auto_subscribe(self, updated_fields, values=None):
        self._add_follower(values)
        return super(Task, self).message_auto_subscribe(updated_fields, values=values)

    #ex01: add worker as follower
#     def _add_follower(self, vals):
#         if vals.get('worker_id'):
#             subtype = self.env.ref('mail.mt_note')
#             worker = self.env['res.partner'].browse(vals['worker_id'])
#             self.message_subscribe(partner_ids=worker.ids, subtype_ids=subtype.ids)

    #ex02: add worker as follower, no need to subscribe to subtype
    def _add_follower(self, vals):
        if vals.get('worker_id'):
            worker = self.env['res.partner'].browse(vals['worker_id'])
            self.message_subscribe(partner_ids=worker.ids)

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'worker_id' in init_values:
            return 'ex02.task_assign'
        return super(Task, self)._track_subtype(init_values)
