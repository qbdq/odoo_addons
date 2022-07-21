# -*- coding: utf-8 -*-
{
    'name': "cabinet",

    'summary': """
        This is a custom module for managing a doctor cabinet
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "To be ",


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work corre   ctly
    'depends': ['base','calendar'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/partner_inherit.xml',
        'views/calendar_event.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
