# -*- coding: utf-8 -*-
{
    'name': "helpdesk ticket custom",

    'summary': """
        This module creates new models and fields to extend the functionality of the helpdesk tickets
        """,

    'description': """
        Module that extends functionality in the helpdesk module
    """,

    'author': "Andirent - Julián Toscano",
    'website': "https://www.andirent.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'helpdesk',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['helpdesk',
                'helpdesk_fsm',
                'website',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/website_form.xml',
        'views/views.xml',
    ],
}
