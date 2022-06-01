from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    plaque_id = fields.Many2one(comodel_name='stock_production_plaque', string='Placa')
    fee_unit = fields.Float(string='Tarifa', digits='Product fee')
    contract_date = fields.Date(strins='Fecha de contrato',
                                help='Indica la fecha que se realiza el contrato asociada a dicha transferencia')
    contract_date_end = fields.Date(strins='Fecha de contrato final',
                                    help='Indica la fecha que se realiza el contrato asociada a dicha transferencia')

    # Realaciona la placa/tarifa/fecha de contrato con numero de serie desde el modelo stock move line
    def compute_plaque_id(self):
        data = self.env['stock.move.line'].search([('lot_id', '=', self.ids),
                                                   ('product_id', '=', self.product_id.ids),
                                                   ('qty_done', '=', self.product_qty)], limit=1, order='id DESC')
        self.plaque_id = data.plaque_id.id
        self.fee_unit = data.fee_unit
        self.contract_date = data.contract_date
        self.contract_date_end = data.contract_date_end









