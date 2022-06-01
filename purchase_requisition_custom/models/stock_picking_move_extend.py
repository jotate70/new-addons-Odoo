from odoo import fields, models, api
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
import json


class stock_picking_extend(models.Model):
    _inherit = 'stock.move'

    image_product = fields.Binary(string='Imagen', related='product_id.image_1920')
    stage = fields.Integer(string='Etapa')
    account_analytic_id = fields.Many2one(comodel_name='account.analytic.account', string='Cuenta Analítica',
                                          related='location_dest_id.account_analytic_id')
    available_origin_location = fields.Float(string='Disponible', related='product_id.free_qty',
                                             help='Muestra la cantidad disponible que está sin reservar')

    standard_price = fields.Float(
        string='Costo Unitario', company_dependent=True,
        digits='Product Price',
        groups="base.group_user",
        related='product_id.standard_price',
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
            In FIFO: value of the last unit that left the stock (automatically computed).
            Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
            Used to compute margins on sale orders.""")

    standard_price_t = fields.Float(
        string='Costo',
        compute='_compute_standard_price_t',
        help="""Costo unitario por cantidad de productos."""
    )

    fee_unit = fields.Float(string='Tarifa', digits='Product fee')
    fee_subtotal = fields.Float(compute='_compute_fee_subtotal', string='Subtotal Tarifa')
    contract_date = fields.Date(strins='Fecha de contrato', related='picking_id.contract_date',
                                help='Indica la fecha que se realiza el contrato asociada a dicha transferencia')
    contract_date_end = fields.Date(strins='Fecha de contrato final', related='picking_id.contract_date_end',
                                help='Indica la fecha que se realiza el contrato asociada a dicha transferencia')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', related='picking_id.currency_id')

    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                line._compute_amount()
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            currency = order.currency_id or order.partner_id.property_purchase_currency_id or self.env.company.currency_id
            order.update({
                'amount_untaxed': currency.round(amount_untaxed),
                'amount_tax': currency.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    # Optiene el costo subtotal
    @api.depends('standard_price')
    def _compute_standard_price_t(self):
        for rec in self:
            rec.standard_price_t = rec.standard_price*rec.product_uom_qty

    # Optiene la tarifa subtotal
    @api.depends('fee_unit')
    def _compute_fee_subtotal(self):
        for rec in self:
            rec.fee_subtotal = rec.fee_unit * rec.quantity_done

    #   crea registross en stock_move_line
    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        self.ensure_one()
        # apply putaway
        location_dest_id = self.location_dest_id._get_putaway_strategy(self.product_id, quantity=quantity or 0, packaging=self.product_packaging_id).id
        vals = {
            'move_id': self.id,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'location_id': self.location_id.id,
            'location_dest_id': location_dest_id,
            'picking_id': self.picking_id.id,
            'company_id': self.company_id.id,
            'fee_unit': self.fee_unit,
        }
        if quantity:
            rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            uom_quantity = self.product_id.uom_id._compute_quantity(quantity, self.product_uom, rounding_method='HALF-UP')
            uom_quantity = float_round(uom_quantity, precision_digits=rounding)
            uom_quantity_back_to_product_uom = self.product_uom._compute_quantity(uom_quantity, self.product_id.uom_id, rounding_method='HALF-UP')
            if float_compare(quantity, uom_quantity_back_to_product_uom, precision_digits=rounding) == 0:
                vals = dict(vals, product_uom_qty=uom_quantity)
            else:
                vals = dict(vals, product_uom_qty=quantity, product_uom_id=self.product_id.uom_id.id)
        if reserved_quant:
            vals = dict(
                vals,
                location_id=reserved_quant.location_id.id,
                lot_id=reserved_quant.lot_id.id or False,
                package_id=reserved_quant.package_id.id or False,
                owner_id =reserved_quant.owner_id.id or False,
            )
        return vals

