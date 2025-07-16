from odoo import api, fields, models,_
from odoo.exceptions import UserError


class HelpdeskWizard(models.TransientModel):
    _name = 'helpdesk.wizard'
    _description = 'Helpdesk Wizard'

    user_id = fields.Many2one('res.users', string="User")
    ticket_ids = fields.Many2many('helpdesk.ticket', string="Tickets", required=True)

    def assign_users(self):
        if self.company_id.id != 1:
            for rec in self:
                if not rec.ticket_ids:
                    raise UserError(_("Please select at least one ticket to assign a user."))
                for line in rec.ticket_ids:
                    line['user_id'] = rec.user_id.id
            # rec.ticket_ids.write({'user_id': [user.user_id.id for user in rec.ticket_ids]})

