# -*- coding: utf-8 -*-
{
    'name': 'Account Extra',
    'summary': '''Incluye facturación con GTI''',
    'version': '13.0.0.0',
    'author': 'Xavier Méndez (xmmendezy@gmail.com)',
    'license': 'AGPL-3',
    'category': 'Account',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'views/account_move_reversal.xml',
        'views/account_move.xml',
		'views/account_move_economic_activity.xml',
        'views/account_tax.xml',
		'views/account_res_currency.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
