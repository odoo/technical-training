from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive'),
    ]

    # Basic Information
    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ], copy=False)
    validity = fields.Integer(default=7, string='Validity (days)')
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string='Deadline')
    
    # Relationships
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', string='Property Type', store=True)
    
    # Computed Methods
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            # Use create_date if available, otherwise use today as fallback
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                # Calculate validity based on deadline and create_date
                base_date = record.create_date.date()
                delta = record.date_deadline - base_date
                record.validity = delta.days
            elif record.date_deadline:
                # If no create_date, use today as fallback
                today = fields.Date.today()
                delta = record.date_deadline - today
                record.validity = delta.days
    
    # Button Action Methods (Public - no underscore prefix)
    def action_accept(self):
        for record in self:
            # Refuse all other offers for this property first
            other_offers = record.property_id.offer_ids.filtered(lambda o: o.id != record.id)
            other_offers.write({'status': 'refused'})
            
            # Accept this offer
            record.status = 'accepted'
            
            # Set buyer and selling price on the property
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True
    
    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True
    
    # CRUD Method Overrides
    @api.model_create_multi
    def create(self, vals_list):
        # Handle both single record and batch creation
        if not isinstance(vals_list, list):
            vals_list = [vals_list]
        
        # Process each record in the batch
        for vals in vals_list:
            # Get the property record
            property_id = vals.get('property_id')
            if property_id:
                property_record = self.env['estate.property'].browse(property_id)
                
                # Check if offer price is higher than existing offers
                existing_offers = property_record.offer_ids
                if existing_offers:
                    max_existing_price = max(existing_offers.mapped('price'))
                    if vals.get('price', 0) <= max_existing_price:
                        raise UserError(f"Offer price must be higher than existing offers. Current highest offer: {max_existing_price}")
                
                # Set property state to 'Offer Received'
                property_record.state = 'offer_received'
        
        # Always call super() to maintain the flow
        return super().create(vals_list)
    
    