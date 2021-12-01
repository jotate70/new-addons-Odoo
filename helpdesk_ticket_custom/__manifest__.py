# -*- coding: utf-8 -*-
#
# Autor: Julián Toscano
# Desarrollador e implementador Odoo
# Email: jotate70@gmail.com
# Github: jotate70
# Cel. +57 3147754740
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

    'author': "Andirent  Athor: Julián Toscano",
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
                'account_accountant',
                'website_helpdesk_form',
                'contacts',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views_helpdesk_classification.xml',
        'views/views_helpdesk_family.xml',
        'views/views_helpdesk_project.xml',
        'views/views_helpdesk_sub_group.xml',
        'views/views_helpdesk_task_extended.xml',
        'views/views_helpdesk_team_extended.xml',
        'views/views_helpdesk_ticket_extended.xml',
        'views/views_helpdesk_partner_extended.xml',
    ],

    'installable': True,
}
