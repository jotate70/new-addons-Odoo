# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    return_picking_id = fields.Many2one(comodel_name='stock.return.picking', string='Return')
