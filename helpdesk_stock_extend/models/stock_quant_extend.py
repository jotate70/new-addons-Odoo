from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    quantity_transit = fields.Float('Quantity Transit', help='Quantity of products in this quant, in the default unit of measure of the product',
                                    digits='Product Unit of Measure')

    # # Restricción de cantidad
    # @api.constrains('quantity_transit')
    # def _compute_constrains_available(self):
    #     for line in self:
    #         if line.available_quantity > line.quantity_transit:
    #             raise UserError('La cantidad limite que puedes agregar es %s.' % line.available_quantity)


