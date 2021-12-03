# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

# heredamos del modelo de tickets de mesa ayuda
class helpdesk_ticket_extended(models.Model):
    _inherit = 'helpdesk.ticket'

    x_visibility_related = fields.Boolean(string='Campo oculto', related='team_id.x_visibility', store=True, readonly=True)
    x_classification = fields.Many2one(comodel_name='helpdesk_classification', string='clasificación')
    x_project = fields.Many2one(comodel_name='helpdesk_project', string='Proyecto', required="True")
    x_family = fields.Many2one(comodel_name='helpdesk_family', string='Familia', required="True")
    x_sub_group = fields.Many2one(comodel_name='helpdesk_sub_group', string='Sub grupo', required="True")

    # Se aplica un decorador que detecta el cambio del campo x_familia
    @api.onchange('x_family')
    def _domain_ochange_x_familia(self):
        return{'domain': {'x_sub_group': [('x_family', "=", self.x_family.id)]}}

# heredamos del modelo helpdesk team
class helpdesk_team_inherit(models.Model):
    _inherit = 'helpdesk.team'

    x_visibility = fields.Boolean(string='Visibilidad de clasificación')

# heredamos del modelo proyectos de mesa de ayuda al modelo usuarios
class helpdesk_users(models.Model):
    _inherit = 'res.users'

    x_project = fields.Many2many(comodel_name='helpdesk_project', relation='helpdesk_project_relation', columnn1='id', columnn2='name', string='Proyecto')

# Se hereda el campo de ticket en el modelo de tareas
class project_task(models.Model):
    _inherit = 'project.task'

    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', help='Ticket this task was generated from')

# Se crea modelo clasificación
class helpdesk_classification(models.Model):
    _name = 'helpdesk_classification'
    _description = 'Clasificación en mesa de ayuda'

    name = fields.Char(string='Nombre', required="True")
    x_code = fields.Char(string='Código', required="True")

    # Restricción a nivel de SQL
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'La clasificación ya existe'),
    ]

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

# Se crea modelo family
class helpdesk_family(models.Model):
    _name = 'helpdesk_family'
    _description = 'Familia en mesa de ayuda'

    name = fields.Char(string='Nombre', required="True")
    x_code = fields.Char(string='Código', required="True")
    x_sub_group = fields.Many2many(comodel_name='helpdesk_sub_group', relation='helpdesk_relation_f_a_s', columnn1='id', columnn2='name', string='Sub grupo', readonly='False')

    # Restricción a nivel de SQL
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'La familia ya existe'),
    ]

# Se crea modelo sub grupo
class helpdesk_sub_group(models.Model):
    _name = 'helpdesk_sub_group'
    _description = 'Sub grupo en mesa de ayuda'

    name = fields.Char(string='Nombre', required="True")
    x_code = fields.Char(string='Código', required="True")
    x_family = fields.Many2one(comodel_name='helpdesk_family', string='Familia')

    # Restricción a nivel de SQL
    _sql_constraints = [
        ('x_code_unique', 'UNIQUE(x_code)', 'El codigo debe ser unico'),
    ]


