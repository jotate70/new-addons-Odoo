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
    'name': 'Subscriptions Extend',

    'summary': '',

    'description': """,
    """,

    'author': "Company: Andirent SAS,  Author: Julián Toscano, https://www.linkedin.com/in/jotate70/",
    'website': "https://www.andirent.co",

    'version': '0.1',
    'category': 'Sales/Subscriptions',

    'depends': [
        'sale_subscription',
        'purchase_requisition_custom',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/sale_order_type_views.xml',
        'views/sale_subscription_views.xml',
        'views/employee_extend_view.xml',
    ],

    'demo': [
    ],

    # 'assets': {
    #     'web.assets_backend': [
    #         'sale_subscription/static/src/js/tours/sale_subscription.js',
    #         'sale_subscription/static/src/scss/sale_subscription_backend.scss',
    #     ],
    #     'web.assets_frontend': [
    #         'sale_subscription/static/src/js/portal_subscription.js',
    #     ],
    # }

    'installable': True,
    'application': True,
    # 'license': 'OEEL-1',
}
