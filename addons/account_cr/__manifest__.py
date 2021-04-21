# -*- coding: utf-8 -*-
{
	# Module information
    "name": "Account CR",
    "version": "14.0.1.0.0",
    "category": "Account",
    "sequence": "1",
    "summary": """Facturación en Costa Rica""",
    "description": """Facturación en Costa Rica""",
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
        'views/account_move.xml',
    ],
    'installable': True,
    "auto_install": False,
}
