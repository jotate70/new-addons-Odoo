
from odoo import models, fields, api

# Inherit
class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    _description = "income third party"

    add_third = fields.Boolean()
    invoice_line_ids2 = fields.One2many('account.invoice', 'invoice_id2', ' income third party')


    # Valores ingresos para terceros
    product_id2 = fields.Many2one('product.product', string='Producto',
                                  ondelete='cascade',
                                  help="Select a product which will use "
                                       "analytic account specified in "
                                       "analytic default (e.g. create new "
                                       "customer invoice or Sales order if we "
                                       "select this product, it will "
                                       "automatically take this as an "
                                       "analytic account)")
    account_id2 = fields.Many2one(
        comodel_name="account.account",
        string="Cuenta",
        required=True,
        help="The account of the forecast line is only for informative purpose",
    )
    invoice_id2 = fields.Many2one('account.invoice', string='Referencia de pago',
                                 ondelete='cascade', index=True)
    journal_id2 = fields.Many2one('account.journal', string='Diario de pago',
                                 required=True,
                                 domain=[('type', 'in', ('bank', 'cash'))])
    account_analytic_id2 = fields.Many2one('account.analytic.account',
                                          string='Cuenta analitica')
    analytic_tag_ids2 = fields.Many2many('account.analytic.tag',
                                        string='Etiqueta analitica')
    quantity2 = fields.Float()
    price_total2 = fields.Monetary()

    # Campo computado
    @api.multi
    def compute_field(self):
        self.field_total = self.price_total2 + self.amount_total

    field_total = fields.Float('Total a pagar:', compute=compute_field)

# Income thrid party model
class Income_thrid_party(models.Model):
    _name = "account.income_thrid_party_table"
    _description = "Income thrid party"

    name = fields.Char()
    product_id = fields.Char()
    account_id = fields.Char()
    invoice_id2 = fields.Char()
    journal_id2 = fields.Char()
    account_analytic_id2 = fields.Char()
    analytic_tag_ids2 = fields.Char()
    quantity = fields.Float()
    price_total = fields.Float()










