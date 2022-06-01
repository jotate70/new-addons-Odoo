from odoo import fields, models, api

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    location = fields.Many2one(comodel_name='location_warehouse',
                               string='Locación', related='warehouse_id.location_id',
                               help='Muestra la ubicación de la ciudad/locación del producto',
                               )
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='Almacen', store=True,
                                          related='location_id.warehouse_id', help='Almacen origen')
    transit_location_id = fields.Many2one(comodel_name='stock.location', string='Ubicación de transito',
                                          related='location_id.transit_location_id',
                                          help='Solo se permite una ubicación de transito por almacen')
    fee_unit = fields.Float(string='Tarifa unitaria', related='lot_id.fee_unit')
    plaque_id = fields.Many2one(comodel_name='stock_production_plaque', string='Placa', related='lot_id.plaque_id')

    contract_date = fields.Date(strins='Fecha de contrato', related='lot_id.contract_date',
                                help='Indica la fecha que se realiza el contrato asociada a dicha transferencia')

    contract_date_end = fields.Date(strins='Fecha de contrato', related='lot_id.contract_date_end',
                                help='Indica la fecha que se realiza el contrato asociada a dicha transferencia')






