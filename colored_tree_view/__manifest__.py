# -*- coding: utf-8 -*-
{
    'name': "Colored Tree View",

    'summary': "Change Your Tree Records Color",

    'description': """
        Each record of a tree can be colored according to a few simple conditions.
        The arch description of the tree may have one of the background-x attribute to add a brilliant background color.
         """,

    'author': "Ali Badran",
    'website': "https://github.com/ali-badran-95",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '1.3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/assets.xml',
    ],

    'images': ['static/description/assets/images/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
