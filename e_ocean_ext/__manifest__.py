# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Affinity E Ocean EXT',
    'version': "1.0.0",

    'summary': '',
    'description': """""",
    'depends': ['base', 'helpdesk'],
    'data': [
          
          'views/subtype_view.xml',
          'views/helpdesk_inherited_view.xml',
          'data/sequence.xml',
          'security/ir.model.access.csv',
          'wizard/helpdesk_wizard.xml',
          
          
        ],
   
    'installable': True,
    'application': True,
    'auto_install': False,
    'License': 'LGPL-3'
}