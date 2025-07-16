# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Affinity HR EXT',
    'version': "1.0.0",

    'summary': '',
    'description': """""",
    'depends': ['base','hr_appraisal','hr_recruitment','mail','hr'],
    # ,'project'
    'data': [
        
           'security/ir.model.access.csv',
           'views/ext.xml',
           'views/applicant.xml',
           'data/report_paperformat.xml',
           'data/email_templates.xml',
           # 'data/onboarding_email_templates.xml',
           'report/employee_exit_clearance_template.xml',
           'report/employee_exit_clearance_report.xml',
        #    'wizard/sale_wizard.xml',
        #    'data/sequence.xml',
          
          
        ],

    
    'installable': True,
    'application': True,
    'auto_install': False,
    'License': 'LGPL-3'
}