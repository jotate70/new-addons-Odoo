from odoo import fields, models, api
import json


class stock_picking_extend(models.Model):
    _inherit = 'stock.move'

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

    fee_unit = fields.Float(string='Tarifa unitaria', digits='Product Price')
    # fee_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)

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


