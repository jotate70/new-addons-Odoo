# -*- coding: utf-8 -*-
#
# Julián Toscano
# Desarrollador e implementador Odoo
# Email: jotate70@gmail.com
# Bogotá,Colombia
#
#
{
    'name': "helpdesk ticket custom",

    'summary': """
        This module creates new models and fields to extend the functionality of the helpdesk tickets,
        and website form
        """,

    'description': """
        Module that extends functionality in the helpdesk module and add website form
    """,

    'author': "Andirent, author: Julián Toscano",
    'website': "https://www.andirent.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'helpdesk',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': [
                'base',
                'helpdesk',
                'industry_fsm',
                'website_helpdesk_form',
                'website',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/helpdesk_teams.xml',
        'views/views_helpdesk_classification.xml',
        'views/views_helpdesk_family.xml',
        'views/views_helpdesk_project.xml',
        'views/views_helpdesk_sub_group.xml',
        'views/views_helpdesk_task_extended.xml',
        'views/views_helpdesk_team_extended.xml',
        'views/views_helpdesk_ticket_extended.xml',
        'views/views_helpdesk_users_extended.xml',
    ],

    'installable': True,
}
