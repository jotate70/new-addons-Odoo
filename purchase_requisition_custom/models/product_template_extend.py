from odoo import fields, models, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    stock_quant = fields.One2many(comodel_name='stock.quant', inverse_name='product_tmpl_id',
                                  string='Inventario disponible')
    available_stock = fields.Float(string='Disponible', compute='_compute_available_stock')
    # available_stock_filter = fields.Boolean(string='Disponible', compute='_compute_available_stock_filter', compute_sudo=False)
    # available_stock2 = fields.Float(string='Disponible', compute='_compute_available_stock')
    # demo = fields.Char('demo')

    # @api.depends(
    #     'product_variant_ids.qty_available',
    #     'product_variant_ids.virtual_available',
    #     'product_variant_ids.incoming_qty',
    #     'product_variant_ids.outgoing_qty',
    #     'product_variant_ids.available_stock2',
    # )
    # def _compute_quantities(self):
    #     res = self._compute_quantities_dict()
    #     for template in self:
    #         template.qty_available = res[template.id]['qty_available']
    #         template.virtual_available = res[template.id]['virtual_available']
    #         template.incoming_qty = res[template.id]['incoming_qty']
    #         template.outgoing_qty = res[template.id]['outgoing_qty']
    #         template.available_stock2 = res[template.id]['available_stock2']
    #
    # def _compute_quantities_dict(self):
    #     variants_available = {
    #         p['id']: p for p in self.product_variant_ids.read(['qty_available', 'virtual_available', 'incoming_qty', 'outgoing_qty', 'available_stock2'])
    #     }
    #     prod_available = {}
    #     for template in self:
    #         qty_available = 0
    #         virtual_available = 0
    #         incoming_qty = 0
    #         outgoing_qty = 0
    #         available_stock2 = 0
    #         for p in template.product_variant_ids:
    #             qty_available += variants_available[p.id]["qty_available"]
    #             virtual_available += variants_available[p.id]["virtual_available"]
    #             incoming_qty += variants_available[p.id]["incoming_qty"]
    #             outgoing_qty += variants_available[p.id]["outgoing_qty"]
    #             available_stock2 += variants_available[p.id]["available_stock2"]
    #         prod_available[template.id] = {
    #             "qty_available": qty_available,
    #             "virtual_available": virtual_available,
    #             "incoming_qty": incoming_qty,
    #             "outgoing_qty": outgoing_qty,
    #             "available_stock2": available_stock2,
    #         }
    #     return prod_available
    #
    # def _search_available_stock2(self, operator, value):
    #     domain = [('available_stock', operator, value)]
    #     product_variant_query = self.env['product.product']._search(domain)
    #     return [('product_variant_ids', 'in', product_variant_query)]


    # @api.depends('available_stock')
    # def _compute_available_stock_filter(self):
    #     for rec in self:
    #         if rec.available_stock > 0:
    #             rec.available_stock_filter = True
    #         else:
    #             rec.available_stock_filter = False

    # Indica el stock en bodegas internas
    def _compute_available_stock(self):
        for rec1 in self:
            data = rec1.env['stock.quant'].sudo().search([('product_tmpl_id', '=', rec1.ids), ('usage', '=', 'internal'),
                                                          ('location_id.usage', '=', 'internal'),
                                                          ('available_quantity', '>', 0.0)])
            if data:
                for rec2 in data:
                    rec1.available_stock += rec2.available_quantity
            else:
                rec1.available_stock = 0











