# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    picking_ids = fields.Many2many('stock.picking', string="Return Orders", copy=False)

    def compute_picking_ids(self, pickings):
        self.picking_ids = pickings

