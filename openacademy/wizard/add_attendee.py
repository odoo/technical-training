# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'

    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('openacademy.session', string="Sessions", required=True, default=_default_sessions)
    attendee_ids = fields.Many2many('res.partner', string="Attendees", domain=[('is_company', '=', False)])

    @api.multi
    def subscribe(self):
        for session in self.session_ids:
            already_subscribed = session.attendee_ids.mapped('partner_id')
            for partner in self.attendee_ids:
                if partner not in already_subscribed:
                    self.env['openacademy.attendee'].create({
                        'partner_id' : partner.id,
                        'session_id' : session.id,
                        'course_id'  : session.course_id.id,
                        'state'      : 'confirmed',
                    })
        return {}