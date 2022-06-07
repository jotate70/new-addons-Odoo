# -*- coding: utf-8 -*-
#
# Autor: Julián Toscano
# Email: jotate70@gmail.com
# Desarrollador y funcional Odoo
# Github: jotate70
# Cel. +57 3147754740
#
#

{
    'name': "l10n_co_invoice",

    'summary': """
        Facturas Terceros""",

    'description': """
        Modulo que agrega la funcion de ingresos para terceros
    """,
    'author': "Lion Consulting SAS  Author: Julián Toscano",
    'website': "https://www.lionconsulting.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['account','base','account','account_standard_report'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/account_view.xml',
        'views/account_invoice_third_views.xml',
        'report/invoice_customer_third_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
            ],
}