# ©  2021 Radovan Skolnik <radovan@skolnik.info>
# -*- coding: utf-8 -*-
#
# Autor: Julián Toscano
# Email: jotate70@gmail.com
# Desarrollador y funcional Odoo
# Github: jotate70
# Cel. +57 3147754740
# https://www.linkedin.com/in/jotate70/
#
#

{
    'name': "Website sale category custom",

    'summary': """
        15.0.1 Add the categories in the layout of a product in ecommerce.
        """,

    'description': """
        
    """,

    'author': "Julián Toscano",

    'category': 'Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website_sale',
                ],
    'data': [
        'views/templates.xml',
    ],

    'installable': True,
    'application': True,

    'license': 'LGPL-3',

}

