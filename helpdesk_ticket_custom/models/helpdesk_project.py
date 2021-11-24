# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

# Se crea modelo proyecto
class helpdesk_project(models.Model):
    _name = 'helpdesk_project'
    _description = 'Proyecto en mesa de ayuda'

    name = fields.Char(string='Nombre', required="True")
    x_code = fields.Char(string='Código', required="True")

    # Restricción a nivel de SQL
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'El proyecto ya existe'),
    ]
