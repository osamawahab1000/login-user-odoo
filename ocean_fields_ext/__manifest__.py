# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Affinity Ocean Fields EXT',
    'version': "1.0.0",

    'summary': '',
    'description': """""",
    'depends': ['base', 'sale'],
    'data': [
            'data/ir_sequence_data.xml',
           'security/ir.model.access.csv',
           'views/fiscal_year.xml',
           'views/ocean_affinity.xml',
           'wizard/mailing_wizard.xml'
          
          
        ],
   
    'installable': True,
    'application': True,
    'auto_install': False,
    'License': 'LGPL-3'
}