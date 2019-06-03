from odoo import api, fields, models
from odoo.exceptions import Warning

class Partner(models.Model):
    # _name = 'openacademy.partner'
    # _description = 'Partner'
    _inherit = 'res.partner'

    # name = fields.Char('Name', required=True)

    instructor = fields.Boolean(default=False)
    session_ids = fields.Many2many('openacademy.session', string='Attended Sessions', readonly=True)

    # if instructur = true show field ? 

    max_student = fields.Integer('Number of student')
