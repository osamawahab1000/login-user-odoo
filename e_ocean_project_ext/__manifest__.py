# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Affinity Project EXT',
    'version': "1.0.0",

    'summary': '',
    'description': """""",
    'depends': ['base','project','approvals'],
    'data': [
        
        #    'security/ir.model.access.csv',
           'views/ext.xml',
           'views/approval_ext.xml',
        #    'views/revel_product.xml',
        #    'wizard/sale_wizard.xml',
           'data/sequence.xml',
          
          
        ],

#     'assets': {
    # 'web.assets_backend': [
        # 'e_ocean_project_ext/static/src/js/disable_kanban_drag.js',
#     ],
# },

    
    'installable': True,
    'application': True,
    'auto_install': False,
    'License': 'LGPL-3'
}