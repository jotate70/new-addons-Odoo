# -*- coding: utf-8 -*-

from odoo import models, fields

class l10n_co_contacts(models.Model):
    _inherit = 'res.partner'

    shareholding_structure = fields.Selection([('1', 'Accionista'),
                                               ('2', 'No Accionista')],
                                                string='Composición Accionaria',
                                                help='Indica si es accionista de la compañia, con una participación mayor al 10% ',
                                                store=True, default='2')

    share_percentage = fields.Float(string='% de participación',
                                    help='Establece el porcentaje de participación del accionista')

    tax_auditor = fields.Many2one(comodel_name='res.partner', string='Revisor Fiscal', help='Auditor a cargo')

    auditor_document_type = fields.Many2one(comodel_name='l10n_latam.identification.type', string='Tipo de documento',
                                            related='tax_auditor.l10n_latam_identification_type_id', help='Tipo de documento')

    auditor_document = fields.Char(string='Documento', related='tax_auditor.vat',
                                   help='Documento del revisor fiscal a cargo en la compañia')

    accountant = fields.Many2one(comodel_name='res.partner', string='Contador', help='Contador a cargo')

    accountant_document_type = fields.Many2one(comodel_name='l10n_latam.identification.type', string='Tipo de documento',
                                            related='accountant.l10n_latam_identification_type_id', help='Tipo de documento')

    accountant_document = fields.Char(string='Documento',
                                      related='accountant.vat', help='Documento de contador a cargo')

    # responsible_tax_auditor = fields.Boolean(string='Es revisor fiscal',
    #                                          help='Indica si es revisor fiscal de la compañia asociada. NOTA: Campo visible cuando asocia el individual a una compañia')

    # responsible_accountant = fields.Boolean(string='Es Contador',
    #                                         help='Indica si es contador de la compañia asociada. NOTA: Campo visible cuando asocia el individual a una compañia')








