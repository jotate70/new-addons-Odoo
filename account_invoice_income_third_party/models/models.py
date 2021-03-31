
from odoo import models, fields, api

# tabla ingreso para tercero
class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    _description = "income third party"

    add_third = fields.Boolean(strind="income third party")