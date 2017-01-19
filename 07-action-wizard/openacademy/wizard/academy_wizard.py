# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AcademyWizard(models.TransientModel):
    _name = "openacademy.attendee.wizard"
    _description = "Open Academy Attendees Wizard"

    @api.model
    def _default_attendees(self):
        attendee_ids = self._context.get('active_ids')
        attendees = self.env['res.partner'].browse(attendee_ids)
        return attendees

    attendee_ids = fields.Many2many('res.partner', string="Attendees", default=_default_attendees)
    session_ids = fields.Many2many('openacademy.session', string="Sessions", required=True)

    @api.multi
    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}