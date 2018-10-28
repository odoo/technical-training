from odoo import api, models,fields

class Book(Models.model):
    _name = 'openacademy.book'
    
    book_name=fields.Char()
    book_id=fields.Integer()
    authors= fields.Char()
    editors=fields.Text()
    year_of_edition=fields.Date()
    ISBN=fields.Text()
    