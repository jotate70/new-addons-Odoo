from odoo import fields, models, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.product'

    stock_quant = fields.One2many(comodel_name='stock.quant', inverse_name='product_id',
                                  string='Inventario disponible')
    available_stock = fields.Float(string='Disponible', compute='_compute_available_stock', search='_search_available_stock')

    # Busqueda para campo computado
    def _search_available_stock(self, operator, value):
        vat = []
        if value == 1:
            data = self.env['stock.quant'].sudo().search([('usage', '=', 'internal'),
                                                          ('location_id.usage', '=', 'internal'),
                                                          ('available_quantity', '>', 0.0), ('quantity', '>', 0.0)])
            if data:
                for rec in data:
                    vat.append(rec.product_id.id)
            else:
                vat = []
        return [('id', '=', vat)]

    # Indica el stock en bodegas internas
    def _compute_available_stock(self):
        for rec1 in self:
            data = rec1.env['stock.quant'].sudo().search([('product_id', '=', rec1.ids), ('usage', '=', 'internal'),
                                                          ('location_id.usage', '=', 'internal'),
                                                          ('available_quantity', '>', 0.0)])
            if data:
                for rec2 in data:
                    rec1.available_stock += rec2.available_quantity
            else:
                rec1.available_stock = 0












