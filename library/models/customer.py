from odoo import api,models,fields

class customers(Models.model):
    _name = 'openacademy.customer'
    
    customer_id= fields.Integer()
   
    name=fileds.Char()
    address=fileds.Text(string="address")
    emails=fileds.Char(string="Email") 
