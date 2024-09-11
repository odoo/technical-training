from datetime import datetime, timedelta
from odoo import fields, models, Command
from odoo import api
from odoo import exceptions
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "ESTATE Properties"
    _order = "id desc"

    name = fields.Char(string="Title", required=True, help="Property name")
    description = fields.Text(string="Description", help="Property description")
    postcode = fields.Text(string="Postcode", help="Property Post code")
    date_availability = fields.Date(string="Available From",
                                    default=lambda self: (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
                                    copy=False, help="Property Date Availability")

    expected_price = fields.Float(string="Expected Price", required=True, help="Property Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False, help="Property Selling Price")

    bedrooms = fields.Integer(string="Bedrooms", default=2, help="Property Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)", help="Property Living Area")
    facades = fields.Integer(string="Facades", help="Property Facades")
    garage = fields.Boolean(string="Garage", help="Property Garage")
    garden = fields.Boolean(string="Garden", help="Property Garden")
    garden_area = fields.Integer(string="Garden Area", help="Property Garden Area")
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[("North", "North"), ("South", "South"), ("East", "East"), ("West", "West")],
        help="Orientation help to define the garden orientation")

    active = fields.Boolean(string="Active", default=True, help="Property is available")

    state = fields.Selection(
        string="State",
        selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"),
                   ("sold", "Sold"), ("canceled", "Canceled")],
        default="new",
        help="State of the property advertisement")

    # links
    property_type_id = fields.Many2one('estate.property.type', domain="[('id', '!=', False)]", string="Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Tag")

    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user,
                                     help="Salesperson")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False, help="Buyer Person")

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers', help='List of offers')

    # campos computados
    total_area = fields.Integer(string="Total Area (sqm)", compute='_compute_total_area')

    best_price = fields.Float(string="Best Offer", compute='_compute_best_offer')

    # campo compañia si se tienen 2 o más
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company,
                                 help="Company related to this property")

    # constraints

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'A property expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'A property selling price must be positive'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        """
            Compute and update total area.
        """
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        """
            Compute and update best offer
        """
        for record in self:
            try:
                record.best_price = max(record.offer_ids.mapped('price'))
            except ValueError:
                record.best_price = None

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_sold_property(self):
        for record in self:
            if record.state == 'canceled':
                # cancelard propiedad
                raise exceptions.UserError("canceled property cannot be sold")
            elif record.state != 'offer_accepted':
                # Ya se vendio joven 
                raise exceptions.UserError("You must accept an offer before make a property as sold")
            else:
                record.state = 'sold'

        return True
        
    def action_prueba(self):
        for record in self:
            if record.state == 'canceled':
                # cancelada
                raise exceptions.UserError("canceled property cannot be sold")
            elif record.state != 'offer_accepted':
                # not se acepta ofeertas
                raise exceptions.UserError("You must accept an offer before make a property as sold")
            else:
                record.state = 'sold'

        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                # venida
                raise exceptions.UserError("sold property cannot be canceled")
            else:
                record.state = 'canceled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property_record in self:
            if not float_is_zero(property_record.selling_price, precision_digits=1):
                if float_compare(property_record.selling_price, 0.9 * property_record.expected_price,
                                 precision_digits=2) == -1:
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price!")
                else:
                    pass
            else:
                pass

    @api.ondelete(at_uninstall=False)
    def _check_property_state(self):
        for property_record in self:
            if property_record.state not in ['new', 'canceled']:
                raise UserError("Only New or Canceled property can be deleted!")
            else:
                pass
