from odoo import fields, models, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    stock_quant = fields.One2many(comodel_name='stock.quant', inverse_name='product_tmpl_id',
                                  string='Inventario disponible')
    available_stock = fields.Integer(string='Stock disponible', compute='_compute_available_stock')

    # Indica el stock en bodegas internas
    @api.depends('stock_quant')
    def _compute_available_stock(self):
        data = self.env['stock.quant'].sudo().search([('product_tmpl_id', '=', self.ids), ('usage', '=', 'internal'),
                                                      ('quantity', '!=', 0)])
        if data:
            for rec in data:
                self.available_stock += rec.available_quantity
        else:
            self.available_stock = 0






