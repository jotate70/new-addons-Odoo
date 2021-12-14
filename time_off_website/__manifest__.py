# -*- coding: utf-8 -*-
{
    'name': "time_off_website",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        module that adds time-off website form
    """,

    'author': "Andirent  Author: Julián Toscano",
    'website': "http://www.andirent.co",

    'category': 'holidays',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_holidays',
                'website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

    'license': 'LGPL-3',
    'installable': True,
}
