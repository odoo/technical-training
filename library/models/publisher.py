# -*- coding: utf-8 -*-
from odoo import fields, models


class Editor(models.Model):
    _name = 'library.publisher'
    _description = 'Publisher'

    name = fields.Char()
