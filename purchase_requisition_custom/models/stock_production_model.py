from odoo import fields, models, api, exceptions
from odoo.exceptions import UserError, ValidationError

class Productionplaque(models.Model):
    _name = 'stock_production_model'

    name = fields.Char(string='Model', required=True, help="Unique Plaque", index=True)
    ref = fields.Char(string='Internal Reference', help="Internal reference number in case it differs from the manufacturer's model number")
    lot_ids = fields.One2many(comodel_name='stock.production.lot', inverse_name='model_id', string='Lot/Serial')

    # SQL constraints
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'El modelo ya existe'),
    ]
