# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError

class l10n_co_contacts(models.Model):
    _inherit = 'res.partner'

    shareholding_structure = fields.Selection([('1', 'Accionista'),
                                               ('2', 'No Accionista')],
                                                string='Composición Accionaria',
                                                help='Indica si es accionista de la compañia, con una participación mayor al 10% ',
                                                store=True, default='2')

    share_percentage = fields.Float(string='% de participación',
                                    help='Establece el porcentaje de participación del accionista')

    tax_auditor = fields.Many2one(comodel_name='res.partner', string='Revisor Fiscal', help='Revisor fiscal responsable en la compañia',
                                  domain="[('responsible_tax_auditor','=', True)]")

    auditor_document_type = fields.Many2one(comodel_name='l10n_latam.identification.type', string='Tipo de documento',
                                            related='tax_auditor.dc_type', help='Tipo de documento')

    auditor_document = fields.Char(string='Documento', related='tax_auditor.dc',
                                   help='Documento del revisor fiscal a cargo en la compañia')

    accountant = fields.Many2one(comodel_name='res.partner', string='Contador', help='Contador responsable en la compañia',
                                 domain="[('responsible_accountant','=', True)]")

    accountant_document_type = fields.Many2one(comodel_name='l10n_latam.identification.type', string='Tipo de documento',
                                            related='accountant.dc_type', help='Tipo de documento')

    accountant_document = fields.Char(string='Documento',
                                      related='accountant.dc', help='Documento de contador a cargo')

    responsible_tax_auditor = fields.Boolean(string='Es revisor fiscal',
                                             help='Indica si es revisor fiscal de compañia. NOTA: Solo visisble para individuales')

    responsible_accountant = fields.Boolean(string='Es Contador',
                                            help='Indica si es contador responsable de compañia. NOTA: Solo visisble para individuales')

    dc_type = fields.Many2one(comodel_name='l10n_latam.identification.type',
                                               string='Tipo de documento',
                                               help='Tipo de documento')

    dc = fields.Char(string='Número de ocumento', help='Número de Documento')

    # Evita dejar registro en los campos dc y dc_type cuando no está activo revisor o contador
    @api.onchange('responsible_tax_auditor', 'responsible_accountant')
    def _onchange_document(self):
        if self.responsible_tax_auditor == False and self.responsible_accountant == False:
            self.write({'dc_type': False})
            self.write({'dc': False})

    # Restricción a nivel de SQL
    _sql_constraints = [
        ('dc_unique', 'UNIQUE(dc)',
         'El número de identificación ya existe, por favor mirar en la pestaña Sagrilaft en contactos'),
    ]
















