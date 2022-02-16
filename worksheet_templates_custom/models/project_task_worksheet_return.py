# -*- coding: utf-8 -*-

from odoo import models, fields, api


class worksheet_templates_custom(models.Model):
    _name = 'project_task_worksheet_return'
    _inherit = 'industry_fsm_report'
    _description = 'project task worksheet return'

    project_task_worksheet = fields.Char(string='Hoja de trabajo', related='worksheet.template', store=True,
                                   help='Indica el tipo de hoja de trabajo')
    return_date = fields.Date(string='Fecha de devolución', help='Agregar la fecha que se realiza la devolución')
    customer = fields.Char(string='Cliente', related='res.partner', store=True,
                                   help='Cliente que se le realiza la devolución')
    helpdesk_project = fields.Char(string='Proyecto', related='helpdesk_project.name', store=True,
                           help='Proyecto mesa de ayuda asignado')

    helpdesk_project_code = fields.Char(string='Código', related='helpdesk_project.code', store=True,
                                   help='Código del proyecto mesa de ayuda asignado')
    project_task = fields.Char(string='Código', related='project.task', store=True,
                                        help='Tarea relacionado')
    helpdesk_ticket = fields.Char(string='Código', related='helpdesk.ticket', store=True,
                                        help='Tickets relacionado')
    photo = fields.Binary(string="Foto", help='Cargar fotografia de la devolución, como registro')

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
