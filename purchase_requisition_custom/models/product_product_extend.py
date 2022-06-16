# -*- coding: utf-8 -*-
import operator as py_operator
from odoo import fields, models, api, _

OPERATORS = {
    '<': py_operator.lt,
    '>': py_operator.gt,
    '<=': py_operator.le,
    '>=': py_operator.ge,
    '=': py_operator.eq,
    '!=': py_operator.ne
}

class Product(models.Model):
    _inherit = "product.product"

    available_stock = fields.Integer(string='Stock disponible')

    # Indica el stock en bodegas internas
    @api.depends('stock_quant')
    def _compute_available_stock(self):
        data = self.env['stock.quant'].search([('product_id', '=', self.ids), ('usage', '=', 'internal'), ('default_code', '=', self.default_code)])
        for rec in data:
            self.available_stock += rec.available_quantity

    qty_available_origin_warehouse = fields.Float(
        'Quantity On Hand', compute='_compute_quantities', search='_search_qty_available',
        digits='Product Unit of Measure', compute_sudo=False,
        help="Current quantity of products.\n"
             "In a context with a single Stock Location, this includes "
             "goods stored at this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, or any "
             "of its children.\n"
             "stored in the Stock Location of the Warehouse of this Shop, "
             "or any of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type.")

    def _search_qty_available_origin_warehouse(self, operator, value):
        # In the very specific case we want to retrieve products with stock available, we only need
        # to use the quants, not the stock moves. Therefore, we bypass the usual
        # '_search_product_quantity' method and call '_search_qty_available_new' instead. This
        # allows better performances.
        if not ({'from_date', 'to_date'} & set(self.env.context.keys())):
            product_ids = self._search_qty_available_origin_warehouse_new(
                operator, value, self.env.context.get('lot_id'), self.env.context.get('owner_id'),
                self.env.context.get('package_id'), self.env.context.get('warehouse_id')
            )
            return [('id', 'in', product_ids)]
        return self._search_product_quantity(operator, value, 'qty_available')

    def _search_qty_available_origin_warehouse_new(self, operator, value, lot_id=False, owner_id=False, package_id=False, warehouse_id=False):
        ''' Optimized method which doesn't search on stock.moves, only on stock.quants. '''
        product_ids = set()
        domain_quant = self._get_domain_locations()[0]
        if lot_id:
            domain_quant.append(('lot_id', '=', lot_id))
        if owner_id:
            domain_quant.append(('owner_id', '=', owner_id))
        if package_id:
            domain_quant.append(('package_id', '=', package_id))
        if warehouse_id:
            domain_quant.append(('stock_quant_ids.warehouse_id.usage', '=', 'supplier'))
        quants_groupby = self.env['stock.quant'].read_group(domain_quant, ['product_id', 'quantity'], ['product_id'], orderby='id')

        # check if we need include zero values in result
        include_zero = (
            value < 0.0 and operator in ('>', '>=') or
            value > 0.0 and operator in ('<', '<=') or
            value == 0.0 and operator in ('>=', '<=', '=')
        )

        processed_product_ids = set()
        for quant in quants_groupby:
            product_id = quant['product_id'][0]
            if include_zero:
                processed_product_ids.add(product_id)
            if OPERATORS[operator](quant['quantity'], value):
                product_ids.add(product_id)

        if include_zero:
            products_without_quants_in_domain = self.env['product.product'].search([
                ('type', '=', 'product'),
                ('id', 'not in', list(processed_product_ids))],
                order='id'
            )
            product_ids |= set(products_without_quants_in_domain.ids)
        return list(product_ids)

