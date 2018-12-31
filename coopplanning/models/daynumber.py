# -*- coding: utf-8 -*-
from odoo import fields, models


class DayNumber(models.Model):
    _name = 'coopplanning.daynumber'
    _description = 'Day of the Week number'

    name = fields.Char()

    number = fields.Integer("Day Number", help="From 1 to N, When you will instanciate your planning, Day 1 will be the start date of the instance, Day 2 the second, etc...")
    active = fields.Boolean(default=True)
