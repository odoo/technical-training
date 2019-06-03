from odoo import api, fields, models
from odoo.exceptions import Warning


class Books(models.Model):
    # _name = 'library.books'
    _inherit = 'product.product'
    # _description = 'Books'

    # name = fields.Char('Title', required=True)
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    author_ids = fields.Many2many('library.partner', string='Authors')
    date_published = fields.Date()
    isbn = fields.Char('ISBN')
    is_book = fields.Boolean()

    copy_ids = fields.One2many('library.book_copy', 'book_id', string="Book Copies")

class book_copy(models.Model):
    _name = 'library.book_copy'
    _description = 'Book copy'
    _inherits = {'product.product': 'book_id'}
    _rec_name = 'reference'

    book_id = fields.Many2one('product.product', string="Book", required=True)
    reference = fields.Char()

    rent_ids = fields.One2many('library.rental', 'bookcopy_id', string='Rented by')

    

