# -*- coding: utf-8 -*-
{
    'name': "hr holidays website form",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Andirent",
    'website': "https://www.andirent.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_holidays',
                'website',
                ],

    'installable': True,
    'application': True,

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/website_time_off_form_template.xml',
        'views/website_menu.xml',
        'views/time_off_submited.xml',
    ],

    'license': 'LGPL-3',
}
