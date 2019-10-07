# -*- coding: utf-8 -*-
{
    'name': "Project Housing Model",
    'summary': """Construction Project Housing""",
    'description': """

    """,
    'author': "Dennis Boy Silva - Agilis Enterprise Solutions, Inc.",
    'website': "http://www.agilis.com.ph",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project',
    'version': '12.1',
    # any module necessary for this one to work correctly
    'depends': ['base',
                'project',
                'product',
                'website_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'data/sequence.xml',
        # 'views/book_profile.xml',
        # 'views/book_management.xml',
        'views/housing_project.xml',
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    'auto_install': False,
}
