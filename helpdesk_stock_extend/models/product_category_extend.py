from odoo import fields, models, api
from odoo.exceptions import UserError

class ProductCategory(models.Model):
    _inherit = "product.category"

    return_location_id = fields.Many2many(comodel_name='stock.location', relation='x_product_category_return_location_rel',
                                          column1='product_category_id', column2='stock_location_id',
                                          string='Ubicaciones de devolución', help='Ubicaciones para devolcuciones que puede usar la categoria del producto',
                                          domain="[('usage', '=', 'transit'), ('return_location', '=', True)]", required=True)

    # Restricción ubicación de retorno por ciudad
    @api.constrains('return_location_id')
    def _compute_constrains_return_location(self):
        for line in self.return_location_id:
            for line2 in self.return_location_id:
                if line != line2:
                    if line.location_id2 == line2.location_id2:
                        raise UserError(
                            'Ya esxiste una ubicación de devoluciones en %s. solo puedes agregar una ubicación de devolución por locación.' % line.location_id2.name)

