# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

# heredamos del modelo de tickets de mesa ayuda
class helpdesk_ticket_extended(models.Model):
    _inherit = 'helpdesk.ticket'

    x_project = fields.Many2one(comodel_name='helpdesk_project', string='Project', required="True")
    x_family = fields.Many2one(comodel_name='helpdesk_family', string='Familia', required="True")
    x_sub_group = fields.Many2one(comodel_name='helpdesk_sub_group', string='Sub grupo', required="True")

    # Se aplica un decorador que detecta el cambio del campo x_familia
    @api.onchange('x_family')
    def _domain_ochange_x_familia(self):
        return{'domain': {'x_sub_group': [('x_family', "=", self.x_family.id)]}}

# heredamos del modelo proyectos de mesa de ayuda al modelo usuarios
class helpdesk_users(models.Model):
    _inherit = 'res.users'

    x_project = fields.Many2many(comodel_name='helpdesk_project', relation='helpdesk_project_relation', columnn1='id', columnn2='name', string='Project')

# creamos modelo proyecto
class helpdesk_project(models.Model):
    _name = 'helpdesk_project'
    _description = 'Familia en mesa de ayuda'

    name = fields.Char(string='Nombre del proyecto', required="True")
    x_code = fields.Char(string='Código del proyecto', required="True")

    # Restricción a nivel de SQL
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'El proyecto ya existe'),
    ]

    _sql_constraints = [
        ('x_code_unique', 'UNIQUE(x_code)', 'El codigo debe ser unico'),
    ]

# creamos modelo familia
class helpdesk_family(models.Model):
    _name = 'helpdesk_family'
    _description = 'Familia en mesa de ayuda'

    name = fields.Char(string='Nombre de la familia', required="True")
    x_code = fields.Char(string='Código de la familia', required="True")
    x_sub_group = fields.Many2many(comodel_name='helpdesk_sub_group', relation='helpdesk_relation_f_a_s', columnn1='id', columnn2='name', string='Familia', readonly='False')

    # Restricción a nivel de SQL
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'La familia ya existe'),
    ]

    _sql_constraints = [
        ('x_code_unique', 'UNIQUE(x_code)', 'El codigo debe ser unico'),
    ]

# creamos modelo subgrupo
class helpdesk_sub_group(models.Model):
    _name = 'helpdesk_sub_group'
    _description = 'Sub grupo en mesa de ayuda'

    name = fields.Char(string='Nombre del sub grupo', required="True")
    x_code = fields.Char(string='Código del sub grupo', required="True")
    x_family = fields.Many2one(comodel_name='helpdesk_family', string='Family', required="True")

    # Restricción a nivel de SQL
    _sql_constraints = [
        ('x_code_unique', 'UNIQUE(x_code)', 'El codigo debe ser unico'),
    ]


