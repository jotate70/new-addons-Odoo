# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    # subscription_management = fields.Selection(string='Subscription Management', selection=[('create', 'Creation'), ('renew', 'Renewal'), ('upsell', 'Upselling')],
    #                                            default='create',
    #                                            help="Creation: The Sales Order created the subscription\n"
    #                                                 "Upselling: The Sales Order added lines to the subscription\n"
    #                                                 "Renewal: The Sales Order replaced the subscription's content with its own")
    # subscription_count = fields.Integer(compute='_compute_subscription_count')

    sale_order_type = fields.Many2one(string='Tipo de orden', comodel_name='sale_order_type')

    # Action confirm stock picking
    def _action_confirm(self):
        if self.sale_order_type.allow_stock_picking == True:
            self.order_line._action_launch_stock_rule()
            return super(SaleOrder, self)._action_confirm()
        else:
            return

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # subscription_id = fields.Many2one('sale.subscription', 'Subscription', copy=False, check_company=True)
    #
    available_quantity_total = fields.Float(string='Stock', related='product_id.available_stock',
                                            help='Muestra la cantidad disponible que está sin reservar')

