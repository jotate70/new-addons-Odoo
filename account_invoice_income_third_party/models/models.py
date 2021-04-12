
from odoo import models, fields, api

# Inherit
class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    _description = "income third party"

    add_third = fields.Boolean()

    # Valores ingresos para terceros
    product_id2 = fields.Many2one('product.product',
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
        help="The account of the forecast line is only for informative purpose",
    )
    quantity2 = fields.Float()
    price_total2 = fields.Monetary()

    # Campo computado
    @api.multi
    def compute_field(self):
        self.field_total = self.price_total2 + self.amount_total

    field_total = fields.Float(compute=compute_field)

    # Income thrid party model
    class Income_thrid_party(models.Model):
        _name = "account.income_thrid_party_table"
        _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
        _description = "Income thrid party"

        product_id = fields.Char(string='Concepto')
        referencia = fields.Char(string='Referencia')
        account_id = fields.Char(string='Cuenta')
        account_analytic_id = fields.Char('Cuenta analitica')
        analytic_tag_ids = fields.Char('Etiqueta analitica')
        price = fields.Float('Valor')














