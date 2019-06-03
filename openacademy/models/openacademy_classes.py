from odoo import api, fields, models
from odoo.exceptions import Warning

DIFFICULTY = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
]

class Classes(models.Model):
    _name = 'openacademy.class'
    _description = 'Classes'

    name = fields.Char('Title', required=True)

    responsible_id = fields.Many2one('res.partner', string='Responsible')
    sessions_ids = fields.One2many('openacademy.session', 'course_id', string='Sessions')
    difficulty = fields.Selection(DIFFICULTY, string='Difficulty')


