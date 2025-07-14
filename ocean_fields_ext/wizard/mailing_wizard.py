from odoo import api, fields, models,_
from odoo.exceptions import UserError


class MailingContactWizard(models.TransientModel):
    _name = 'mailing.wizard'
    _description = 'Mailing Contact Wizard'

    partner_id = fields.Many2many('res.partner', string="Contacts")
    mailing_list = fields.Many2one('mailing.list', string="Mailing List")
    
    def action_create_contacts(self):
        for partner in self.partner_id:
            self.env['mailing.contact'].create({
                # 'partner_id': partner.id,
                'name': partner.name,
                'email': partner.email,
                'subscription_ids': [(0, 0, {'list_id': self.mailing_list.id})],
            })
