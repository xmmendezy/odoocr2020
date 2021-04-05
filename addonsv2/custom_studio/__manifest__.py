# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Custom Studio",
    'summary': "Custom studio",
    'website': '',
    'description': "",
    'sequence': 75,
    'version': '1.0',
    'depends': [
        'base_automation',
        'base_import_module',
        'mail',
        'web',
        'custo_web_enterprise',
        'web_editor',
        'custom_web_map',
        'custom_web_gantt',
        'sms',
    ],
    'data': [
        'views/assets.xml',
        'views/actions.xml',
        'views/base_import_module_view.xml',
        'views/ir_actions_report_xml.xml',
        'views/ir_model_data.xml',
        'views/templates.xml',
        'views/studio_approval_views.xml',
        'wizard/base_module_uninstall_view.xml',
        'security/ir.model.access.csv',
        'security/studio_security.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'application': True,
    'license': 'AGPL-3',
}
