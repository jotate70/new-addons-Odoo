from odoo import fields, models, api, _

class stock_picking_extend(models.Model):
    _inherit = 'stock.picking'

    ticket_return = fields.Many2one(comodel_name='helpdesk.ticket', string='Return tickets')
