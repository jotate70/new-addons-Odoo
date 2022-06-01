from odoo import fields, models, api


class stock_move_line(models.Model):
    _inherit = 'stock.move.line'

    plaque_id = fields.Many2one(comodel_name='stock_production_plaque', string='Placa')
    fee_unit = fields.Float(string='Tarifa', digits='Product fee')
    fee_subtotal = fields.Float(compute='_compute_fee_subtotal', string='Subtotal Tarifa')
    contract_date = fields.Date(strins='Fecha de contrato', related='picking_id.contract_date',
                                help='Indica la fecha que se realiza el contrato asociada a dicha transferencia')
    contract_date_end = fields.Date(strins='Fecha de contrato final', related='picking_id.contract_date_end',
                                    help='Indica la fecha que se realiza el contrato asociada a dicha transferencia')
    observation = fields.Char(string='Observación')

    # Optiene el tarifa subtotal
    @api.depends('fee_unit')
    def _compute_fee_subtotal(self):
        for rec in self:
            rec.fee_subtotal = rec.fee_unit * rec.qty_done





