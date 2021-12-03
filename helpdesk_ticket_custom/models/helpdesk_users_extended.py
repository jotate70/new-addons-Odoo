# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

# heredamos del modelo usuarios
class helpdesk_users_extended(models.Model):
    _inherit = 'res.users'

    x_project = fields.Many2many(comodel_name='helpdesk_project', relation='helpdesk_project_relation', columnn1='id', columnn2='name', string='Proyecto')
