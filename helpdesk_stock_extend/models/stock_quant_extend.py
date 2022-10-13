from odoo import fields, models, api, _
from odoo.tools.float_utils import float_compare, float_is_zero

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    quantity_transit = fields.Float('Quantity Transit', help='Quantity of products in this quant, in the default unit of measure of the product',
                                    digits='Product Unit of Measure')

