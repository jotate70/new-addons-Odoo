# -*- coding: utf-8 -*-
{
    'name': "Purchase Agreements Custom",

    'summary': """
        15.0.1 module that adds approvals by levels according to the budget of each immediate boss in the purchase requisitions.
        """,

    'description': """
        module that adds approvals by levels according to the budget of each immediate boss in the purchase requisitions.
    """,

    'author': "Andirent  Author: Julián Toscano",
    'website': "https://www.andirent.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase_requisition',
                'hr',
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/employee_extend_view.xml',
        'views/purchase_extend_view.xml',
        'views/purchase_requisition_extend_view.xml',
        'views/users_extend_view.xml',
        # 'data/plan_activity.xml'
    ],

    'installable': True,
    'application': True,

}
