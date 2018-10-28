from odoo import api,models,fields

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    
    responsible_id = fields.Many2one('openacademy.partner', string="Responsible", index=True)
    
    session_ids = fields.One2many(  'openacademy.session', 'course_id', string="Sessions")
    level= fields.Selection([('easy','Easy'),('medium','Medium'),('hard','Hard')],string="Difficulty Level")
