from odoo import fields, models, api


class ModelName(models.Model):
    _inherit = 'res.partner'

    # Restricción a nivel de SQL
    _sql_constraints = [
        ('dc_unique', 'UNIQUE(dc)', 'El número de identificación ya existe, por favor mirar en la pagina Sagrilaft en contactos'),
    ]

    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'El correo ya existe'),
    ]

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'El nombre ya existe'),
    ]

    _sql_constraints = [
        ('vat_unique', 'UNIQUE(vat)', 'El número de identificación ya existe'),
    ]

