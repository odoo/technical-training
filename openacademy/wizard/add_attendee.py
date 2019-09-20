# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models


class AddAttendees(models.TransientModel):
    _name = 'add_attendee.wizard'
    _description = 'Wizard to add attendees to a session'

    @api.model
    def default_get(self, fields):
        res = super(AddAttendees, self).default_get(fields)
        res.update({'attendee_ids': [(6, 0, self._context.get('active_ids', []))]})
        return res

    session_id = fields.Many2one('openacademy.session', string="Sessions", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees", )

    @api.model
    def create(self, vals):
        res = super(AddAttendees, self).create(vals)
        return res

    def subscribe(self):
        for session in self.session_id:
            session.attendee_ids |= self.attendee_ids
        return {}
