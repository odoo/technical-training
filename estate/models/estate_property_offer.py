from datetime import datetime, timedelta
from datetime import date
from odoo import fields, models
from odoo import api
from odoo import exceptions
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Properties Offer"
    _order = "price desc"

    price = fields.Float(string="Price", help="Buyer Offer")
    validity = fields.Integer(string="validity (days)", default=7, help="validity")
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline', help='Validity date')

    status = fields.Selection(
        string="Status",
        selection=[("offer_accepted", "Accept"), ("offer_refused", "Refuse"),],
        copy=False,
        help="State of the property advertisement")
    
    partner_id = fields.Many2one('res.partner', string="Partner", required=True, help="Person who make the offer")
    property_id = fields.Many2one('estate.property', string="Property", required=True, help="Property")

    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    # constraints
    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)', 'An offer price must be strictly positive'),
    ]


    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = date.today() + timedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = record.date_deadline - datetime.now().date()
    
    def action_accept_offer(self):
        for record in self:
            # Reject all others offers
            for offer in record.property_id.offer_ids:
                offer.status = 'offer_refused'
            
            # acceptado
            record.status = 'offer_accepted'

            # Actualizar campos de precios 
            record.property_id.state = record.status
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

            
        
        return True
    
    def action_refuse_offer(self):
        for record in self:
            record.status = 'Refused'
            
        return True
    
    @api.model
    def create(self, vals):
        # Check precio mas bajo que el permitido
        existing_offers = self.env['estate.property.offer'].search([('property_id', '=', vals['property_id']), ('price', '>=', vals['price'])])
        if existing_offers:
            raise ValidationError("The offer price cannot be lower than an existing offer.")
        
        # Oferta recibida al crear la oferta.
        self.env['estate.property'].browse(vals['property_id']).write({'state': 'offer_received'})
        return super().create(vals)