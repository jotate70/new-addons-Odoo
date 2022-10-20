from odoo import fields, models, api
from odoo.exceptions import UserError

class ProductCategory(models.Model):
    _inherit = "product.category"

    transit_location_id_domain = fields.Char(compute='_domain_transit_location_id_product_category', readonly=True, store=False)
    location_id = fields.Many2many(comodel_name='stock.location', relation='x_product_category_stock_location_rel',
                                   column1='product_category_id', column2='stock_location_id',
                                   string='Ubicaciones de transito', help='Ubicación de transito por defecto para las recepciones',
                                   domain="[('usage', '=', 'transit')]")

    location_default = fields.Many2one(comodel_name='stock.location', string='Almacén de transito por defecto',
                                       domain="[('usage', '=', 'transit')]",
                                       help='Puedes indicar el almacen principal, solo se puede selecionar uno,'
                                            'Sirve para indicar la ubicación de transito por defecto, cuando no se tiene'
                                            'una ubicación de transito en categorias de productos')

    # Restricción ubicación de transito por ciudad
    @api.constrains('location_id')
    def _compute_constrains_location(self):
        for line in self.location_id:
            for line2 in self.location_id:
                if line != line2:
                    if line.location_id2 == line2.location_id2:
                        raise UserError('Ya esxiste una ubicación de transito en %s. solo puedes agregar una ubicación de transito por locación.' % line.location_id2.name)
