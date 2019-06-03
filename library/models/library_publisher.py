from odoo import fields, models, api, exceptions


class Editor(models.Model):
    _name = 'library.publisher'
    _description = 'Publisher'

    name = fields.Char()