from odoo import fields, models, api,_
from odoo.exceptions import UserError
from datetime import datetime,timedelta
import logging
from itertools import cycle
from bs4 import BeautifulSoup
import re
_logger = logging.getLogger(__name__)


keywords = [
    '[INTERNAL]', '[internal]', '[Internal]',
    '[EXTERNAL]', '[external]', '[External]',
    'ANNUAL LEAVES', 'annual leaves', 'Annual Leaves',
    'AUTO', 'auto', 'Auto',
    'AUTO REPLY', 'auto reply', 'Auto Reply',
    'AUTOMATIC REPLY', 'automatic reply', 'Automatic Reply',
    'CANCELLED', 'cancelled', 'Cancelled',
    'CAUTIOUS', 'cautious', 'Cautious',
    'LAST WORKING DAY', 'last working day', 'Last Working Day',
    'ON LEAVES', 'on leaves', 'On Leaves',
    'OUT OF OFFICE', 'out of office', 'Out Of Office',
    'SMS GATEWAY ALERT', 'sms gateway alert', 'SMS Gateway Alert',
    'RECALL', 'recall', 'Recall',
    'TEST', 'test', 'Test',
    'TEST EMAIL', 'test email', 'Test Email',
    'UNDELIVERED', 'undelivered', 'Undelivered',
    'UNDELIVERABLE', 'undeliverable', 'Undeliverable',
    'POSTMASTER', 'postmaster', 'Postmaster'
]
email_list = [
    '@eocean.com.pk',
    '@eocean.net'
    # '@affinitysuite.net'
]

subtype_mapping = {
    'Masking': {
        'SMS Delivery Issue': 27,
        'Masking SMS not deliver': 27,

        'Branded SMS Portal': 28,
        'Portal Issue': 28,
        'pk.eocean': 28,
        'Executing sms via portal': 28,
        # 'Outbox option': 28,

        'Add up request': 29,
        'Charge': 29,
        'Recharge': 29,
        'SMS Addition': 29,
        'Add up': 29,
        'Add-up': 29,

        'Mask Request': 30,
        'Add mask': 30,
        'activate mask': 30,
        'remove mask': 30,

        'Promotional Campaign': 31,



        'Others': 32,

        'Log Required': 33,
        'Branded SMS logs': 33,
        'Mask log': 33,
        'Masking logs': 33,
        'outbox option logs': 33,
    },
    'Short Code': {
        'SMS Delivery Issue': 35,
        'SMS not receive': 35,
        'OTP not receive': 35,
        'OTP not receive': 35,
        'OTP': 35,
        'SMS issue': 35,
        'Shortcode SMS': 35,

        'Portal Issue': 34,
        'Reporting': 34,
        'Reporting Portal': 34,
        'Platform.eocean': 34,

        'Short Code Request': 36,
        'Informational Campaign': 37,


        'Others': 39,

        'Top Up Request': 40,
        'Insufficient Balance': 40,
        'Low balance': 40,
         
        'Log Required': 38,
        'Logs': 38,
        'Delivery Logs': 38,
        'DLR report': 38,
        'SMS logs': 38
    },
    'General': {
        'Ported Number': 41,
        'Ported': 41,
        'Convert': 41,
        'MNP': 41,
        'Port out': 41,

        ' IP Whitelisting': 42,
        ' IP ': 42,
        'Timeout error': 42,
        'Timeout': 42,
        'Unauthorize access': 42,
        ' IP whitelist': 42,

        # 'Invoice / Log Reconciliation': 43,
        'Invoice': 43,
        'Payment': 43,
        'Reconciliation': 43
    },
    'IVR': {
        # 'Connectivity Issue': 44,
        'Call Center': 44,
        # 'IVR': 44,
        'VOIP Service': 44,

        'Service Activation': 45,
        'Activate IVR': 45,

        'Service Modification': 46,

        # 'Others': 47,
        'Robo Calls': 47,
        
        'BAHL': 48,
        'Recorded Call': 48,
        'Bank Alhabib Robo Call': 48
    },
    'WABA': {
        'Others': 49,



        'Connectivity Issues': 50,
        'Chat Bot Issues': 51,
        'Agent Login': 52
        # 'Agent Login/Portal Issues': 52
    },
    'International Complaints':{
        # 'International Complaints': 53,
        'International': 53,
        'MNO': 53,
        'OTAC': 53
    },
    'Issue by Eocean':{
        'Issue by Eocean':55,
        'Issue raised by Eocean':55
    },
    'Non-Service/Complaint':{
        'Non-Service/Complaint':54
        
    },
    'V2 Migration':{
        # 'V2 Migration':56,
        'V2':56,
        'V1':56,
        'api.eocean.net':56,
        'New API':56,
        'Old API':56,
        'V3':56 
    },

}






class HelpdeskInherited(models.Model):
    _inherit = "helpdesk.ticket"

    subtype = fields.Many2many('subtype', string = "Sub type",  domain="[('type', '=', ticket_type_id)]")
    agent_response_date = fields.Datetime("First Agent Response Date")
    date_close = fields.Datetime("Close Date")
    department_id = fields.Many2many("hr.department", string = "Department Responsible")
    closed_by = fields.Many2one('res.users',string="Closed By")

    ticket_no = fields.Char(string="Ticket Number", copy=False, readonly=True,index=True)

    to_inprogress_time = fields.Datetime("To In Progress Time")


    to_onhold = fields.Datetime("To Onhold Time")



    to_solved = fields.Datetime("To Solved Time")

    solved_to_closedtime = fields.Datetime("Solved to Closed Time")
    to_reopen = fields.Datetime("To Re Open Time")

    parent_company = fields.Many2one('res.partner',readonly=True)

    ticket_method = fields.Selection(selection=[('email', 'On Email'),('portal', 'On Portal'),('call', 'On Call')],string='Source')
    ticket_unique = fields.Char(string="Is Unique", compute="check_unique")
    responsible_user = fields.Many2one('res.users',string="Responsible User")
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env.company,
        readonly=True
    )

    
    
    def check_unique(self):
         for rec in self:
              rec['ticket_unique'] = " "
              if rec.name:
                    help = self.env['helpdesk.ticket'].search([('name','=',rec.name), ('stage_id', 'not in', [5, 6]), ('id', '!=', rec.id)])
                    if help:
                        for tick in help:
                            if tick.name == rec.name:
                                rec['ticket_unique'] = "Not Unique"
                            else:
                                rec['ticket_unique'] = "Unique"
                    else:
                            rec['ticket_unique'] = "Unique"
                             
                        




    def helpdesk_open_wizard(self,ids):
        
        view = self.env.ref('e_ocean_ext.helpdesk_wizard_form')
        return {
            'name': 'helpdesk Wizard',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': 'helpdesk.wizard',
            'target': 'new',
            'context': {'default_ticket_ids': ids },
        }

    
    def check_online_user(self):
        if self.company_id.id == 1:
            users = []
            team = self.env['helpdesk.team'].search([('id', '=', self.team_id.id)], limit=1)
            if team:
                for member in team.member_ids:
                    if member.status == 'online' and member.setaway == True:
                        users.append(member.id)
                if users:

                    if team.round_robin_index >= len(users):
                        team.round_robin_index = 0

                    online_user_id = users[team.round_robin_index]

                    team.round_robin_index = (team.round_robin_index + 1)

                    self.user_id = online_user_id
                else:
                    self.user_id = None

    def set_ticket_and_priority(self, ticket_type_id, subtypes):
        if self.company_id.id == 1:
            if self.description:
                self.ticket_type_id = ticket_type_id
            if subtypes is not None:
                self.subtype = subtypes
                self.priority = '1' if len(subtypes) > 1 else self.subtype.priority

        if ticket_type_id == 8:
            self.ticket_ref = self.env['ir.sequence'].with_company(self.company_id).next_by_code('helpdesk.masking')
        elif ticket_type_id == 9:
            self.ticket_ref = self.env['ir.sequence'].with_company(self.company_id).next_by_code('helpdesk.sc')
        elif ticket_type_id == 10:
            self.ticket_ref = self.env['ir.sequence'].with_company(self.company_id).next_by_code('helpdesk.gl')
        elif ticket_type_id == 11:
            self.ticket_ref = self.env['ir.sequence'].with_company(self.company_id).next_by_code('helpdesk.ivr')
        elif ticket_type_id == 12:
            self.ticket_ref = self.env['ir.sequence'].with_company(self.company_id).next_by_code('helpdesk.waba')
        elif ticket_type_id == 13:
            self.ticket_ref = self.env['ir.sequence'].with_company(self.company_id).sudo().next_by_code('helpdesk.ic')
        elif ticket_type_id == 14:
            self.ticket_ref = self.env['ir.sequence'].with_company(self.company_id).next_by_code('helpdesk.ibe')
        elif ticket_type_id == 15:
            self.ticket_ref = self.env['ir.sequence'].with_company(self.company_id).next_by_code('helpdesk.ns')
        elif ticket_type_id == 16:
            self.ticket_ref = self.env['ir.sequence'].with_company(self.company_id).next_by_code('helpdesk.mig')

    def triggered_email_based_on_priority(self):
        if self.company_id.id == 1:
            for rec in self:
                subtypes = []
                ticket_type_id = None
                for main_type, subtype_dict in subtype_mapping.items():
                    if rec.description:
                        # if main_type.lower() in rec.description.lower():
                            # ticket_type_id = list(subtype_mapping.keys()).index(main_type) + 8
                            for subtype_keyword, subtype_id in subtype_dict.items():
                                if subtype_keyword.lower() in rec.description.lower():
                                    subtypes.append(subtype_id)
                                    ticket_type_id = list(subtype_mapping.keys()).index(main_type) + 8
                                    # break

                            if ticket_type_id:
                                break

                if subtypes:
                    rec.set_ticket_and_priority(ticket_type_id, subtypes)
                elif not subtypes:
                    rec.set_ticket_and_priority(ticket_type_id, [])



    @api.depends('stage_id','ticket_type_id','subtype')
    def _compute_sla_deadline(self):
        if self.company_id.id != 1:
            return
        for rec in self:
                for sla in rec.sla_ids:
                    for sla_status in rec.sla_status_ids:
                        if sla.start_stage.id == rec.stage_id.id:
                        

                            if sla.start_stage.id == 1 :
                                time = rec.create_date if rec.create_date else fields.Datetime.now()
                                sla_total = sum(slas.time for slas in rec.sla_ids if slas.start_stage.id == 1)
                                total = timedelta(hours=sla_total)
                                if sla_status.sla_id.start_stage.id == 1:
                                    sla_status.update({
                                        'deadline' :  time + total
                                    })
                                    rec.update({
                                        'sla_deadline' :  time + total
                                    })
                            if sla.start_stage.id == 2 :
                                    time = rec.to_inprogress_time if rec.to_inprogress_time else fields.Datetime.now()
                                    sla_total = sum(slas.time for slas in rec.sla_ids if slas.start_stage.id == 2)
                                    total = timedelta(hours=sla_total)
                                    if sla_status.sla_id.start_stage.id == 2:
                                        sla_status.update({
                                            'deadline' :  time  + total
                                        })
                                        rec.update({
                                            'sla_deadline' : time + total
                                        })
                            if sla.start_stage.id == 4 :
                                time = rec.to_solved if rec.to_solved else fields.Datetime.now()
                                sla_total = sum(slas.time for slas in rec.sla_ids if slas.start_stage.id == 4)
                                total = timedelta(hours=sla_total)
                                if sla_status.sla_id.start_stage.id == 4:
                                        sla_status.update({
                                            'deadline' :  time  + total
                                        })
                                        rec.update({
                                            'sla_deadline' : time + total
                                        })



    @api.model
    def create(self, vals):
        vals.setdefault('company_id', self.env.company.id)
        if vals['company_id'] != 1:
            res = super().create(vals)
            if res.ticket_type_id.id == 13:
                res['ticket_ref'] = self.env['ir.sequence'].with_company(vals['company_id']).sudo().next_by_code('helpdesk.ic')
            elif res.ticket_type_id.id == 8:
                res['ticket_ref'] = self.env['ir.sequence'].with_company(vals['company_id']).sudo().next_by_code('helpdesk.masking')
            elif res.ticket_type_id.id == 9:
                res['ticket_ref'] = self.env['ir.sequence'].with_company(self.company_id).sudo().next_by_code('helpdesk.sc')
            elif res.ticket_type_id.id == 10:
                res['ticket_ref'] = self.env['ir.sequence'].with_company(self.company_id).sudo().next_by_code('helpdesk.gl')
            elif res.ticket_type_id.id == 11:
                res['ticket_ref'] = self.env['ir.sequence'].with_company(self.company_id).sudo().next_by_code('helpdesk.ivr')
            elif res.ticket_type_id.id == 12:
                res['ticket_ref'] = self.env['ir.sequence'].with_company(self.company_id).sudo().next_by_code('helpdesk.waba')
            elif res.ticket_type_id.id == 14:
                res['ticket_ref'] = self.env['ir.sequence'].with_company(self.company_id).sudo().next_by_code('helpdesk.ibe')
            elif res.ticket_type_id.id == 15:
                res['ticket_ref'] = self.env['ir.sequence'].with_company(self.company_id).sudo().next_by_code('helpdesk.ns')
            elif res.ticket_type_id.id == 16:
                res['ticket_ref'] = self.env['ir.sequence'].with_company(self.company_id).sudo().next_by_code('helpdesk.mig')
            return res
        res = super().create(vals)
        context = self._context

        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        if not user:
            pass
        else:
            res['parent_company'] = res.partner_id.parent_id.id
        
             
        if self.env.user.has_group('base.group_portal') or self.env.user.has_group('base.group_user'):              
                res.triggered_email_based_on_priority()
                res.check_online_user()
                


                if res.description:
                     if 'ivr' in res.description:
                        if not res.ticket_type_id.id:
                                    res['ticket_type_id'] = 11
                        a1 = str(res.description.lower()).split('ivr')[0].strip()
                        a2 = str(res.description.lower()).split('ivr')[1].strip()
                        words_before_ivr1 = a1.split()
                        words_before_ivr2= a2.split()
                        last_word_before_ivr1 = words_before_ivr1[-1] 
                        last_word_before_ivr2 = words_before_ivr2[-1]
                        # last_word_before_ivr3 = words_before_ivr2[1]
                        ivr_count = res.description.lower().count('ivr')
                        if ivr_count > 1:
                            if 'activate' not in last_word_before_ivr1 or 'activate' not in last_word_before_ivr2: # for ivr
                                current_subtype_ids = res.subtype.ids  
                                new_subtype_ids = current_subtype_ids + [44]  
                                res.write({'subtype': [(6, 0, new_subtype_ids)]})
                        else:
                            if 'activate' not in last_word_before_ivr1:
                                current_subtype_ids = res.subtype.ids  
                                new_subtype_ids = current_subtype_ids + [44]  
                                res.write({'subtype': [(6, 0, new_subtype_ids)]})
                if any(keyword.lower() in res.name.lower()  for keyword in keywords):
                    res.action_archive()
                    res['ticket_type_id'] = None
                    res['subtype'] = None
                    res['user_id'] = None
                    res['stage_id'] = 5                         
                if res.ticket_method == 'email':
                    if not res.ticket_type_id.id:
                        if res.partner_id:
                            
                            if any(eocean_email in res.partner_id.email for eocean_email in email_list):
                                    res.action_archive()
                                    res['ticket_type_id'] = None
                                    res['subtype'] = None
                                    res['user_id'] = None
                                    res['stage_id'] = 5

      
                
        return res
    
    @api.constrains('stage_id','x_studio_remarks')
    def check_usererror(self):
        if self.company_id.id != 1:
            for rec in self:
                if rec.stage_id.id == 4 and not rec.x_studio_remarks:
                    raise UserError("Fill Remarks")
   

    @api.onchange('subtype')
    def check_priority(self):
        if self.company_id.id != 1:
            return
        if len(self.subtype) > 1:
            self.priority = '1'
        else:
            self.priority = self.subtype.priority

    

   


    def write(self,vals):
        for record in self:
            if record.company_id.id != 1:
                return super().write(vals)
        if vals.get('stage_id'):
            if  vals.get('stage_id') == 6:
                vals['date_close'] = datetime.now()
                vals['solved_to_closedtime'] = datetime.now()
                vals['closed_by'] = self.env.user.id
            if  vals.get('stage_id') == 2:
                vals['agent_response_date'] = datetime.now()
                vals['to_inprogress_time'] = datetime.now()
            if  vals.get('stage_id') == 3:
                vals['to_onhold'] = datetime.now()
            if  vals.get('stage_id') == 4:
                vals['to_solved'] = datetime.now()
            if  vals.get('stage_id') == 7:
                vals['to_reopen'] = datetime.now()

        if vals.get('responsible_user'):
            for record in self:
                responsible_user = self.env['res.users'].browse(vals.get('responsible_user'))
                name = vals.get('name') or record.name
                template = self.env['mail.template'].search([('id', '=', 77)], limit=1)
                if template:
                    email_values = {
                        'email_to': responsible_user.login, 
                        'subject':  name,
                    }
                    template.send_mail(self.id, force_send=True, email_values=email_values)

            
        return super(HelpdeskInherited, self).write(vals)


    # 
class MailMail(models.Model):
    _inherit = 'mail.mail'

    # @api.model
    # def create(self, vals):
    #     res = super(MailMail, self).create(vals)
    #     if res.message_type == 'comment' and res.state == 'outgoing':
            
    #         res.cancel()

    #     return res

    def send(self, auto_commit=False, raise_exception=False):
        for rec in self:
            if rec.message_type == 'email':
                rec.state = 'cancel'
            else:
                rec.auto_delete = False
                super(MailMail, rec).send(auto_commit=auto_commit, raise_exception=raise_exception)
        return True


class HelpdeskTeam(models.Model):
    _inherit = 'helpdesk.team'

    round_robin_index = fields.Integer(string="Round Robin Index")



class HelpdeskSlaStatus(models.Model):
    _inherit = 'helpdesk.sla.status'

    @api.depends('ticket_id.create_date', 'sla_id', 'ticket_id.stage_id')
    def _compute_deadline(self):
        for status in self:
            if status.ticket_id.stage_id == 2:
                if status.sla_id:
                    for sla in status.sla_id:
                                if sla.start_stage.id == 2:
                                    sla_total = sum(slas.time for slas in status.sla_id)
                                    total = timedelta(hours=sla_total)
                                    if isinstance(status.ticket_id.sla_deadline, datetime):
                                        time = status.ticket_id.sla_deadline + total
                                        status['deadline'] = time
            super(HelpdeskSlaStatus, self)._compute_deadline()

class HelpdeskSLAInherited(models.Model):
    _inherit = "helpdesk.sla"
    subtype_ids = fields.Many2many('subtype', string = "Sub type",  domain="[('type', 'in', ticket_type_ids)]")
    start_stage = fields.Many2one('helpdesk.stage',string= "Start Stage", domain="[('team_ids', '=', team_id), ('id', 'not in', exclude_stage_ids)]")
