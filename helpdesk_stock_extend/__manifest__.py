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
    'name': "Helpdesk Stock Extend",

    'summary': """

        """,

    'description': """

    """,

    'author': "Company: Andirent SAS,  Author: Julián Toscano, https://www.linkedin.com/in/jotate70/",
    'website': "https://www.andirent.co",

    'category': 'Services/Helpdesk',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'helpdesk_stock',
    ],

    # always loaded
    'data': [
        'wizard/stock_picking_return_extend_views.xml',
    ],
    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}
