from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive'),
    ]

    # Basic Information
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=2))
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ], default='new')
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    # Pricing
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute='_compute_best_price', string='Best Offer')
    
    # Property Details
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area')
    
    # Features
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    
    # People
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    
    # Tags
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    
    # Offers
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    
    # Computed Methods
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0
    
    # Onchange Methods
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    # Button Action Methods (Public - no underscore prefix)
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Cannot cancel a sold property")
            record.state = 'cancelled'
        return True
    
    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cannot sell a cancelled property")
            record.state = 'sold'
        return True
    
    # Python Constraints
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            # Skip validation if selling price is zero (not yet sold)
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            
            # Calculate 90% of expected price
            min_selling_price = record.expected_price * 0.9
            
            # Compare selling price with minimum allowed (90% of expected)
            if float_compare(record.selling_price, min_selling_price, precision_digits=2) < 0:
                raise ValidationError(
                    f"Selling price ({record.selling_price:.2f}) cannot be lower than 90% of expected price ({min_selling_price:.2f})"
                )
    
    # CRUD Method Overrides
    @api.ondelete(at_uninstall=False)
    def _check_property_deletion(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(f"Cannot delete property '{record.name}' because it is in '{record.state}' state. Only 'New' or 'Cancelled' properties can be deleted.")