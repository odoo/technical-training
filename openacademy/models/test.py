# -*- coding:utf-8 -*-
from odoo import api, models,fields

    
class Test(models.Model):
    _name="test.test"
    
    name=fields.Char("test")
    description=fields.Text()

    
