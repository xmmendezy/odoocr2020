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
    'external_dependencies': {
        'python': [
            'stdnum',
            'xmltodict',
        ]
    },
    'data': [
        'views/account_payment.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
