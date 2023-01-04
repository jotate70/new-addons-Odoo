# -*- coding: utf-8 -*-
#
# Autor: Julián Toscano
# Email: jotate70@gmail.com
# https://www.linkedin.com/in/jotate70/
# Desarrollador y funcional Odoo
# Github: jotate70
# Cel. +57 3147754740
#

{
    'name': 'Maintenance Extend',

    'summary': '',

    'description': """,
    """,

    'author': "Company: Andirent SAS,  Author: Julián Toscano, https://www.linkedin.com/in/jotate70/",
    'website': "https://www.andirent.co",

    'version': '0.1',
    'category': 'Manufacturing/Maintenance',

    'depends': [
        'maintenance',
        'stock',
        'purchase_requisition_custom',
        'web_domain_field',
    ],

    'data': [
        # 'security/ir.model.access.csv',
        'views/maintenance_views.xml',
    ],

    'demo': [
    ],

    'installable': True,
    'application': True,
}
