from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "The property offer model"
    _order = "price desc"
    

    # Fields
    
    price = fields.Float()
    validity = fields.Integer(default=7)
    
    # Selectoin Fields
    
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    
    # Relational Fields
    
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    
    property_type_id = fields.Many2one(
        'estate.property.type', related='property_id.property_type_id', store=True)
    
    # Compute Fields
    
    deadline_date = fields.Date(
        compute='_compute_deadline_date', inverse='_inverse_deadline_date')
    
    # Constraints
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The offer price must be strictly positive.'),
    ]

    # Compute Methods
    
    @api.depends("create_date", "validity")
    def _compute_deadline_date(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.deadline_date = date + relativedelta(days=offer.validity)

    def _inverse_deadline_date(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.deadline_date - date).days

    # Action Methods

    def action_accept_offer(self):
        for record in self:
            offers = record.property_id.offer_ids
            for offer in offers:
                offer.action_refuse_offer()
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

            
    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
            if record.status == 'accepted':
                record.property_id.selling_price = None
                record.property_id.buyer_id = None
        return True
    
    # CRUD Methods:

    @api.model
    def create(self, vals):
        properties = self.env['estate.property'].browse(vals['property_id'])
        properties.state = 'offer_received'
        if vals['price'] < properties.best_price:
            raise UserError(f"The offer must be higher than {properties.best_price}")
        return super().create(vals)
