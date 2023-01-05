from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "The real estate properties model"
    _order = "id desc"

    # Fields

    name = fields.Char(required=True, string='Name')
    description = fields.Text(
        default='when duplicated, status and date are not copied')
    postcode = fields.Char(help='this is the postcode')
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)

    # computed fields

    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(
        compute="_compute_best_offer", string='Best Offer', default=0)

    # Selection fields

    state = fields.Selection(
        required=True,
        copy=False,
        default='new',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
    )
    
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
        help="Garden Orientation: North, South, East and West."
    )

    # Relational Fields

    property_type_id = fields.Many2one('estate.property.type')
    
    # user_id = fields.Many2one('res.users')

    property_tag_ids = fields.Many2many('estate.property.tag')

    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    
    sales_person_id = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user)

    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)

    # Constraints

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),

        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price must be strictly positive.'),
    ]
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("The selling price must be at least 90% of the expected price! You must reduce the epected price if you want to accept this offer.")

    # compute methods

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(
                [offer.price for offer in record.offer_ids], default=0)

    # onchange methods

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    # Action Methods

    def action_sold_property(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise UserError("Canceled properties cannot be sold.")

    def action_cancel_property(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise UserError("Sold properties cannot be canceled.")

    # CRUD Methods:
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_canceled(self):
        if any(rec.state not in ('new', 'canceled') for rec in self):
            raise UserError("only new and canceled properties can be deleted!")
