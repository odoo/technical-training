from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + relativedelta(months=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(required=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West') ],
        help="")
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled') ],
        help="")
    active = fields.Boolean(default=1)
    property_type_id = fields.Many2one("estate.property.type")
    seller_id = fields.Many2one("res.partner", string="Seller")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    # the name of 2nd parameter "property_id" is the var string of variable used in offer model
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    # non stored -> not searchable without search method, search="_search_totalarea"
    # store=True
    totalarea = fields.Float(compute="_compute_totalarea")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'The Expected Price should be positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The Selling Price should be positive.')
    ]

    @api.depends("living_area", "garden_area")
    def _compute_totalarea(self):
        for record in self:
            record.totalarea = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == 1:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def set_status_cancel(self):
        if self.state != "sold":
            self.state = "canceled"

    def set_status_sold(self):
        if self.state != "canceled":
            self.state = "sold"