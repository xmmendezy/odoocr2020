# -*- coding: utf-8 -*-
{
    # Module information
    "name": "Account Extra",
    "version": "14.0.1.0.0",
    "category": "Account",
    "sequence": "1",
    "summary": """Facturación en Costa Rica con GTI""",
    "description": """Facturación en Costa Rica con GTI""",
    "license": "LGPL-3",
    # Author
    "author": "Xavier Méndez",
    "website": "https://www.freelancer.com/u/novadragonsoftwa",
    "maintainer": "Xavier Méndez",
    # Dependencies
    'depends': [
        'base',
        'account',
    ],
    # Views
    'data': [
        'views/account_move_reversal.xml',
        'views/account_move.xml',
        'views/account_move_economic_activity.xml',
        'views/account_res_currency.xml',
        'views/account_tax.xml',
        'views/res_partnet.xml',
        'views/product_product.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    "auto_install": False,
}
