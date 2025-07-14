from odoo import fields, models, api, _
from datetime import datetime,timedelta
from odoo.exceptions import UserError
import threading
import logging
import time

_logger = logging.getLogger(__name__)

class CRMStageInherited(models.Model):
    _inherit = "crm.stage"

    time = fields.Float(string='Time')




class CRMLeadInherited(models.Model):
    _inherit = "crm.lead"

    
    start_date = fields.Datetime("Start Date Of Agreement")
    end_date = fields.Datetime("End Date Of Agreement")

    product = fields.Many2many('product.template', string = "Product")
    product_id = fields.Many2one('product.template', string = "Product")
    product_category = fields.Many2many('product.category', string = "Product Categories")

    time_to_change_stage = fields.Float(string='Time to Change Stage')
    attachment1 = fields.Binary(string="Attachment1" , attachment=True)
    attachment2 = fields.Binary(string="Attachment2", attachment=True)
    attachment3 = fields.Binary(string="Attachment3", attachment=True)
    attachment4 = fields.Binary(string="Attachment4", attachment=True)
    attachment5 = fields.Binary(string="Attachment5", attachment=True)
    attachment6 = fields.Binary(string="Attachment6", attachment=True)
    attachment7 = fields.Binary(string="Attachment7", attachment=True)
    attachment8 = fields.Binary(string="Attachment8", attachment=True)
    attachment9 = fields.Binary(string="Attachment9", attachment=True)
    attachment10 = fields.Binary(string="Attachment10", attachment=True)
    attachment11 = fields.Binary(string="Attachment11", attachment=True)
    attachment12 = fields.Binary(string="Attachment12", attachment=True)
    attachment13 = fields.Binary(string="Attachment13", attachment=True)
    attachment14 = fields.Binary(string="Attachment14", attachment=True)
    attachment15 = fields.Binary(string="Attachment15", attachment=True)
    attachment16 = fields.Binary(string="Attachment16", attachment=True)
    checkbox1 = fields.Boolean("Proposal")

    checkbox2 = fields.Boolean("WABA Access Request Form")
    checkbox3 = fields.Boolean("Service Level Agreement")
    checkbox4 = fields.Boolean("VOICEOVER")
    checkbox5 = fields.Boolean("Proposal Go-Ahead")
    checkbox6 = fields.Boolean("Recording Script")
    checkbox7 = fields.Boolean("Service Level Agreement")
    checkbox8 = fields.Boolean("Service Level Agreement")
    checkbox9 = fields.Boolean("Proposal Go-Ahead")
    checkbox10 = fields.Boolean("Client Info Form")
    checkbox11 = fields.Boolean("ShortCode Request Letter")
    checkbox12 = fields.Boolean("NTN")
    checkbox13 = fields.Boolean("SECP Certificate")
    checkbox14 = fields.Boolean("Sample SMS Texts")
    checkbox15 = fields.Boolean("Undertaking")
    checkbox16 = fields.Boolean("Company Profile")
    agreement_signed = fields.Boolean("Agreement Signed 1")
    agreement_signed_2 = fields.Boolean("Agreement Signed 2")
    deadline = fields.Datetime(string='Time Limit to close the stage',compute="_compute_deadline")
    deadline_1 = fields.Datetime(string='Expected Closing')
    remarks = fields.Char(string="Remarks")
    otc = fields.Float(string="OTC")
    mrc = fields.Float(string="MRC")
    total_mrc = fields.Float(string="Total MRC", compute="_compute_calculation")
    qty = fields.Float(string="Quantity")
    price = fields.Float(string="Price")
    total_price = fields.Float(string="Total Price", compute="_compute_total_price")
    current_month = fields.Char(string="Current Month", compute='_compute_current_month')
    total_month = fields.Char(string="Total Month", compute="_compute_total_month")
    fiscal_id = fields.Many2one('fiscal.year',string="Fiscal year")
    uan_price = fields.Float(string="Uan Price")
    uan_qty = fields.Float(string="Uan Qty")
    total_uan = fields.Float(string="Uan", compute="_compute_cal")
    cloud_price = fields.Float(string="Cloud Price")
    cloud_qty = fields.Float(string="Cloud Qty")
    total_cloud = fields.Float(string="Cloud", compute="_compute_cal")
    reordering_price = fields.Float(string="Reordering Price")
    reordering_qty = fields.Float(string="Reordering Qty")
    total_reordering = fields.Float(string="Reordering", compute="_compute_cal")
    pulse_price = fields.Float(string="Pulse Price")
    pulse_qty = fields.Float(string="Pulse Qty")
    total_pulse = fields.Float(string="Pulse", compute="_compute_cal")
    did_price = fields.Float(string="DID Price")
    did_qty = fields.Float(string="DID Qty")
    total_did = fields.Float(string="DID", compute="_compute_cal")
    channel_price = fields.Float(string="Channel Price")
    channel_qty = fields.Float(string="Channel Qty")
    total_channel = fields.Float(string="Channel", compute="_compute_cal")

    conversation_price = fields.Float(string="Conversation Price")
    conversation_qty = fields.Float(string="Conversation Qty")
    total_conversation = fields.Float(string="Conversation", compute="_compute_cal")
    agents = fields.Float(string="Agents")
    total_agents = fields.Float(string="Total Agents", compute="_compute_calculation")
    mau = fields.Float(string="MAU")
    total_mau = fields.Float(string="Total MAU", compute="_compute_calculation")
    support = fields.Float(string="Support")
    total_support = fields.Float(string="Total Support", compute="_compute_calculation")
    re = fields.Float(string="RE")
    total_re = fields.Float(string="Total RE", compute="_compute_calculation")
    pulse_rate = fields.Selection([('1 sec', '1 sec'), ('30 sec', '30 sec'), ('60 sec', '60 sec')],string="Pulse Rate")
    actual_expectation = fields.Float(string="Actual Revenue")

    
    #  <--- Pawan Started Code Here --->

    # received_datetime = fields.Datetime('Received DateTime')
    contracted_datetime = fields.Datetime('Lead Contracted DateTime')
    proposal_datetime = fields.Datetime('Proposal/Quotation DateTime')
    tech_meeting_datetime = fields.Datetime('Technical Meeting DateTime')
    revision_datetime = fields.Datetime('Revision DateTime')
    demo_datetime = fields.Datetime('Demo/Test Account DateTime')
    agreement_datetime = fields.Datetime('Agreement DateTime')
    live_datetime = fields.Datetime('Live Account DateTime')
    golive_datetime = fields.Datetime('Go Live DateTime')
    sent_datetime = fields.Datetime('Invoice Sent DateTime')
    responsible_user = fields.Many2one('res.users',string="Responsible User")
    closed_datetime = fields.Datetime('Closed DateTime')
    tat_failed = fields.Boolean(string="TAT Failed", compute="_check_deadline")
    crm_id_count = fields.Integer(string="CRM ID Count", compute="count_crm")
    document_ids = fields.Many2many('ir.attachment',string="Documents",help="Attach multiple documents related to this record")

    live_account_seq = fields.Char(string='Live Account Ref', readonly=True, copy=False)
    product_categ_id = fields.Many2one('product.category', string='Product Category')

    # @api.onchange('stage_id')
    # def _onchange_stage_id_generate_live_account_sequence(self):
    #     if (
    #         self.stage_id and self.stage_id.name == 'Live Account'
    #         and not self.live_account_seq
    #         and self.partner_id
    #         and self.product_category
    #     ):
    #         # Generate parts
    #         customer_code = self.partner_id.name.replace(' ', '').upper()[:10]
    #         category_code = self.product_categ_id.name.replace(' ', '').upper()[:10]
    #         # Get unique number
    #         seq_number = self.env['ir.sequence'].next_by_code('crm.lead.live.account') or '00000'
    #         self.live_account_seq = f"{customer_code}/{category_code}/{seq_number}"
    
    def count_crm(self):
        for record in self:
            record['crm_id_count'] = self.env['account.move'].search_count([('crm_id', '=', record.id)])
            

    def action_open_out_invoices(self):
        for rec in self:
            partner = rec.partner_id.id
            crm = rec.id
            deal_owner = rec.user_id.name
            deal_owner = rec.user_id.name
            deal_stage = rec.stage_id.id
            domain = rec.email_from
            product_category = [(6,0,rec.product_category.ids)]
            product = rec.product_id.id
            invoice_lines = [(0, 0, {'product_id': product, 'quantity': 1, 'price_unit': 100})]
            # partner = rec.partner_id.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoices',
            'view_mode': 'form',
            'res_model': 'account.move',
            'domain': [('move_type', '=', 'out_invoice'), ('journal_id', '=', 1)],
            'context': dict(self.env.context, default_move_type='out_invoice',default_invoice_line_ids = invoice_lines ,default_product_category= product_category,default_deal_stage=deal_stage,default_domain= domain,default_deal_owner=deal_owner,default_partner_id =partner ,default_invoice_date = datetime.now(),default_crm_id= crm, default_journal_id=1),
            'target': 'current',  # Opens in the same window
        }

    # @api.onchange('product_id')
    # def change_value(self):
    #     for rec in self:
    #         product = rec.product_id.id
    #         if rec.product_id.id != product:
    #             rec['total_uan'] = 0
    #             rec['total_cloud'] = 0
    #             rec['total_reordering'] = 0
    #             rec['total_pulse'] = 0
    #             rec['total_did'] = 0
    #             rec['total_channel'] = 0
    #             rec['total_conversation'] = 0
    #             rec['total_mrc'] = 0
    #             rec['total_agents'] = 0
    #             rec['total_mau'] = 0
    #             rec['total_support'] = 0
    #             rec['total_re'] = 0
    #         rec['total_price'] = 0
            

    # @api.onchange('total_mrc','total_price','otc', 'stage_id')
    # def expected_revenue(self):
    #     for rec in self:
    #         if rec.total_mrc and rec.total_price and rec.otc and rec.stage_id.id == 3:
    #             rec['expected_revenue'] = float(rec.total_mrc) + rec.total_price + rec.otc

    @api.depends('uan_price','uan_qty','cloud_price','cloud_qty','reordering_price','reordering_qty','pulse_price','pulse_qty','did_price','did_qty','channel_price','channel_qty','conversation_price','conversation_qty')
    def _compute_cal(self):
        for rec in self:
            rec['total_uan'] = 0
            rec['total_cloud'] = 0
            rec['total_reordering'] = 0
            rec['total_pulse'] = 0
            rec['total_did'] = 0
            rec['total_channel'] = 0
            rec['total_conversation'] = 0
            if rec.uan_price and rec.uan_qty:
                rec['total_uan'] = rec.uan_price * rec.uan_qty
            if rec.cloud_price and rec.cloud_qty:
                rec['total_cloud'] = rec.cloud_price * rec.cloud_qty
            if rec.reordering_price and rec.reordering_qty:
                rec['total_reordering'] = rec.reordering_price * rec.reordering_qty
            if rec.pulse_price and rec.pulse_price:
                rec['total_pulse'] = rec.pulse_price * rec.pulse_qty
            if rec.did_price and rec.did_qty:
                rec['total_did'] = rec.did_price * rec.did_qty
            if rec.channel_price and rec.channel_qty:
                rec['total_channel'] = rec.channel_price * rec.channel_qty
            if rec.conversation_price and rec.conversation_qty:
                rec['total_conversation'] = rec.conversation_price * rec.conversation_qty

    @api.depends('total_month','mrc','agents','mau','support','re')
    def _compute_calculation(self):
        for rec in self:
            rec['total_mrc'] = 0
            rec['total_agents'] = 0
            rec['total_mau'] = 0
            rec['total_support'] = 0
            rec['total_re'] = 0
            if rec.total_month and rec.mrc:
                rec['total_mrc'] = float(rec.total_month) * rec.mrc
            if rec.total_month and rec.agents:
                rec['total_agents'] = float(rec.total_month) * rec.agents
            if rec.total_month and rec.mau:
                rec['total_mau'] = float(rec.total_month) * rec.mau
            if rec.total_month and rec.support:
                rec['total_support'] = float(rec.total_month) * rec.support
            if rec.total_month and rec.re:
                rec['total_re'] = float(rec.total_month) * rec.re
                
                
    @api.depends('qty','price')
    def _compute_total_price(self):
        for rec in self:
            rec['total_price'] = 0
            if rec.qty and rec.price:
                rec['total_price'] = rec.price * rec.qty
    
    @api.depends('current_month')
    def _compute_current_month(self):
        for record in self:
            record.current_month = datetime.now().strftime('%B %Y')

    @api.depends('fiscal_id.month_name', 'current_month')
    def _compute_total_month(self):
        for record in self:
            if record.fiscal_id.month_name and record.current_month:
                current_date = datetime.strptime(record.current_month, '%B %Y')
                end_date = datetime.strptime(record.fiscal_id.month_name, '%B %Y')

                total_months = ((end_date.year - current_date.year) * 12 + (end_date.month - current_date.month))

                record.total_month = str(total_months)
            else:
                record.total_month = '0'

    @api.onchange('product')
    def get_product(self):
        for rec in self:
           if rec.product:
               rec['product_id'] = rec.product[0].id
                

  
    @api.onchange('stage_id')
    def deadline_com(self):
        for rec in self:
            if rec.deadline:
                rec.update({
                        'deadline_1': rec.deadline
                    })
    

    # def write(self, value):
    #     res = super(CRMLeadInherited, self).write(value)
    #     raise UserError("TEST")
    #     for rec in self:
    #         # Check conditions for stage_id and product_id
    #         if rec.stage_id.id in (5,6,7,8,9,10,11) and rec.product_id.id in (5,6):
    #             # Safely calculate expected_revenue by handling potential None values
    #             rec['expected_revenue'] = float(rec.total_mrc) + float(rec.total_price) + float(rec.otc)

    #     return res


    def write(self, vals):
            # Store original values before write for access after super()
            original_stage_id = vals.get('stage_id')

            # Handle datetime and probability assignments
            if original_stage_id:
                stage_map = {
                    1: {'probability': 10.0},
                    2: {'probability': 20.0, 'contracted_datetime': datetime.now()},
                    3: {'probability': 30.0, 'proposal_datetime': datetime.now()},
                    4: {'probability': 40.0, 'tech_meeting_datetime': datetime.now()},
                    5: {'revision_datetime': datetime.now()},
                    6: {'demo_datetime': datetime.now()},
                    7: {'probability': 80.0, 'agreement_datetime': datetime.now()},
                    8: {'live_datetime': datetime.now()},  # Live Account
                    9: {'probability': 100.0, 'golive_datetime': datetime.now()},
                    10: {'sent_datetime': datetime.now()},
                    11: {'closed_datetime': datetime.now()},
                }

                # Apply matching updates
                if original_stage_id in stage_map:
                    vals.update(stage_map[original_stage_id])

            # Call super first to ensure write succeeds
            res = super(CRMLeadInherited, self).write(vals)

            # Now handle sequence logic after write
            if original_stage_id == 8:  # Live Account stage
                for lead in self:
                    if (
                        not lead.live_account_seq and
                        lead.partner_id and
                        lead.product_category
                    ):
                        customer_code = lead.partner_id.name.replace(' ', '').upper()[:10]
                        category_code = lead.product_category[0].name.replace(' ', '').upper()[:10]
                        seq_number = self.env['ir.sequence'].next_by_code('crm.lead.live.account') or '00000'
                        lead.live_account_seq = f"{customer_code}/{category_code}/{seq_number}"

            return res



    # #  <--- Pawan Ended Here --->

    # # @api.onchange('time_crm')
    def _compute_deadline(self):
        for rec in self:
            rec['deadline'] = False
            sta = self.env['crm.stage'].search([('id', '=', rec.stage_id.id)])
            if sta:
                tim = None
                if sta.id == 1:
                    tim = rec.create_date
                elif sta.id == 2:
                    tim = rec.contracted_datetime
                elif sta.id == 3:
                    tim = rec.proposal_datetime
                elif sta.id == 4:
                    tim = rec.tech_meeting_datetime
                elif sta.id == 5:
                    tim = rec.revision_datetime
                elif sta.id == 6:
                    tim = rec.demo_datetime
                elif sta.id == 7:
                    tim = rec.agreement_datetime
                elif sta.id == 8:
                    tim = rec.live_datetime
                elif sta.id == 9:
                    tim = rec.golive_datetime
                elif sta.id == 10:
                    tim = rec.sent_datetime
                elif sta.id == 11:
                    tim = rec.closed_datetime

                if tim:  # Check if tim is not False or None
                    time = rec.stage_id.time
                    total = timedelta(hours=time)
                    rec.update({
                        'deadline': tim + total
                    })
                else:
                    rec.update({
                        'deadline': False
                    })

    def _check_deadline(self):
        for rec in self:
            rec.tat_failed = False
            if rec.deadline_1:
                # Compare deadline with current time
                current_time = datetime.now()
                if rec.deadline_1 < current_time:
                    rec.tat_failed = True
                else:
                    rec.tat_failed = False


    @api.onchange('stage_id')
    def _check_agreement_signed(self):
        for record in self:
            if record.stage_id.id in (8,9,10,11):
                if not record.agreement_signed and not record.agreement_signed_2:
                    
                    record['tag_ids'] = [(4, 1)]
                else:
                    record['tag_ids'] = [(5, 0, 0)]  
            if record.stage_id.id == 7:
                if not record.agreement_signed  and not record.agreement_signed_2:
                    
                    record['tag_ids'] = [(5, 0, 0)]  

    @api.constrains('stage_id')
    def one_product(self):
        for rec in self:
           if rec.stage_id.id == 2 and len(rec.product) >=2:
               raise UserError("Only Single product should be move to next stage")
               




    @api.constrains('partner_id','email_from','phone','product_category','partner_name','checkbox1', 'checkbox2', 'checkbox3', 'checkbox4','checkbox5','checkbox6','checkbox7','checkbox8','checkbox9','checkbox10','checkbox11','checkbox12','checkbox13','checkbox14','checkbox15','checkbox16', 'stage_id')
    def not_required(self):
        for rec in self:
            current_user = self.env.user
            if not current_user.id == 78:
                if not rec.partner_id or not rec.email_from or not rec.phone or not rec.product_category or not rec.partner_name:
                    raise UserError("Customer, Email, Phone, Product Categories and Company Name fields all should be filled")
                
                
                if rec.stage_id.id in (8,9,10,11):
                    if rec.product_id.id in(10,13,14):
                        if not rec.checkbox1 or not rec.checkbox2 or not rec.checkbox3:   
                            raise UserError(" Checkboxes field is not filled")
                    if rec.product_id.id in(7,8,9):
                        if not rec.checkbox4 or not rec.checkbox5 or not rec.checkbox6 or not rec.checkbox7:   
                            raise UserError(" Checkboxes field is not filled")
                    if rec.product_id.id in(5,6):
                        if not rec.checkbox8 or not rec.checkbox9 or not rec.checkbox10 or not rec.checkbox11 or not rec.checkbox12 or not rec.checkbox13 or not rec.checkbox14 or not rec.checkbox15 or not rec.checkbox16:   
                            raise UserError(" Checkboxes field is not filled")
            
            
            

                
    # @api.constrains('checkbox1', 'checkbox2', 'checkbox3', 'checkbox4','checkbox5','checkbox6','checkbox7','checkbox8','checkbox9','checkbox10', 'stage_id')
    # def _check_checkbox_signed(self):
    #     for record in self:
    #         if record.stage_id.id == 8:
                
    #             if not record.checkbox1 or not record.checkbox2 or not record.checkbox3 or not record.checkbox4 or not record.checkbox5 or not record.checkbox6 or not record.checkbox7 or not record.checkbox8 or not record.checkbox9 or not record.checkbox10: 
    #                 raise UserError(" Checkboxes field is not filled")
                
    def start_stage_timer(self):
        current_stage = self.stage_id.id
        end_stage = 10  

        while current_stage <= end_stage:
            # time.sleep(2)
            self.stage_id = current_stage
            time.sleep(2)
            current_stage += 1

    


  

    
class ResPartnerInherited(models.Model):
    _inherit = 'res.partner'
    
    desc_company = fields.Text("Description Of Company")
    ass_company = fields.Char("Associated Company")

    # poc_name = fields.Char("POC Name")
    poc_contact_no = fields.Char("Associated Company")
    poc_email_add = fields.Char("POC Email Address")
    domain = fields.Char("Domain")
    # comp_web_add = fields.Char("Company Website Address")
    comp_social_link = fields.Char("Company Social Link")
    nature_of_bus = fields.Selection([('manufacturing', 'Manufacturing'), ('retail', 'Retail'), ('service', 'Service'), ('wholesale', 'WholeSale')])
    KAM = fields.Many2one("res.partner", string = "KAM")
    kam_id = fields.Many2one("res.users", string = "KAM")
    cust_success_manager = fields.Char("Customer Success Manager")
    csm_id = fields.Many2one("res.users", string = "Customer Success Manager")
    intrested_service = fields.Char("Intrested Service/Product")
    intrested_service_id = fields.Many2many('product.template',string="Service/Product")
    company_size = fields.Integer("Company Size")
    how_they_reached_us = fields.Many2one('utm.source', string = "How They Reached Us")
    date_of_first_eng = fields.Datetime("Date Of First Engagement")

    contact_email = fields.Char("Contact Email")
    first_name = fields.Char("First Name")
    last_name = fields.Char("Last Name")
    contact_owner = fields.Char("Contact Owner")
    principle = fields.Char('Principle')
    product_cat_id = fields.Many2many('product.category', string='Product Category')
    unique_num = fields.Char('Unique Number')

    @api.constrains('name', 'id','domain')
    def on_name(self):
        for rec in self:
            if rec.name and rec.id and rec.domain:
                normalized_name = rec.name.lower()
                normalized_domain = rec.domain.lower()
                partners = self.env['res.partner'].search([('id', '!=', rec.id)
                ])
                for partner in partners:
                    if partner.name and partner.domain:
                        if (partner.name.lower() == normalized_name) and  (partner.domain.lower() == normalized_domain):
                            raise UserError("A contact with the name and domain already exists.")


    @api.model 
    def create(self,vals):
        res = super(ResPartnerInherited,self).create(vals)
        if res.email:
            parent = self.env['res.partner'].search([('id','!=',res.id),('domain','=',str(res.email).split('@')[1])])
        # elif res.x_studio_email:
        #     parent = self.env['res.partner'].search([('id','!=',res.id),('domain','=',str(res.x_studio_email).split('@')[1])])
            
            res['parent_id'] = parent.id
        return res


class AccountMoveInherited(models.Model):
    _inherit = 'account.move'

    product_category = fields.Many2many('product.category', string="Product Categories")
    crm_id = fields.Many2one('crm.lead', string="CRM ID")
    product_id = fields.Many2many('product.template', string="Products")
    deal_stage = fields.Many2one('crm.stage', string="Deal Stage")
    domain = fields.Char("Domain")
    deal_owner = fields.Char("Deal Owner")
    live_account_seq = fields.Char(string="CRM Sequence")

    @api.model
    def create(self, vals):
        res = super().create(vals)

        # Case 1: Fetch via invoice_origin → sale.order
        sale_order = self.env['sale.order'].search([('name', '=', res.invoice_origin)], limit=1)
        if sale_order and sale_order.opportunity_id:
            crm = sale_order.opportunity_id
        else:
            # Case 2: fallback via live_account_seq if available
            crm = self.env['crm.lead'].search([('live_account_seq', '=', vals.get('live_account_seq'))], limit=1) if vals.get('live_account_seq') else False

        if crm:
            res.crm_id = crm.id
            res.deal_stage = crm.stage_id.id
            res.domain = crm.email_from
            res.invoice_user_id = crm.user_id.id
            res.deal_owner = crm.user_id.name
            res.product_id = [(6, 0, crm.product.ids)]
            res.product_category = [(6, 0, crm.product_category.ids)]
            res.partner_id = crm.partner_id.id

            # Optional: populate invoice lines
            res.invoice_line_ids = [(5, 0, 0)]  # clear existing
            if crm.product_id:
                res.invoice_line_ids = [(0, 0, {
                    'product_id': crm.product_id.id,
                    'quantity': crm.qty or 1,
                    'price_unit': crm.price or 0,
                    'name': crm.product_id.name
                })]

        return res

class SaleOrderInherited(models.Model):
    _inherit = 'sale.order'
    
    deal_name = fields.Char("Description Of Company")
    product_category = fields.Many2many('product.category',string="Product Categories")

    product_id = fields.Many2many('product.template',string="Products")
    pipeline = fields.Char("Pipeline")
    deal_stage = fields.Many2one('crm.stage',string="Deal Stage")
    domain = fields.Char("Domain")
    amount = fields.Float("Amount")
    currency = fields.Char("Currency")
    close_date = fields.Datetime("Close Date")
    deal_owner = fields.Char("Deal Owner")
    deal_type = fields.Char("Deal Type")

    priority = fields.Selection([('low', 'Low Priority'), ('medium', 'Medium Priority'), ('high', 'High Priority'), ('urgent', 'Urgent')], string= "Priority")
    ass_contact_email = fields.Char("Associated Contact Email")
    ass_company = fields.Char("Associated Company")

    @api.model
    def create(self, vals):
        res = super(SaleOrderInherited, self).create(vals)
        for order in res:
            lead = self.env['crm.lead'].search([('id', '=', res.opportunity_id.id), ('stage_id', '=', 2)], limit=1)
            if lead:
                lead.write({'stage_id': 3})
                # lead.update_stage_on_sale_order()
        lead1 = self.env['crm.lead'].search([('id', '=', res.opportunity_id.id)], limit=1)
        if lead1:
            # raise UserError(str(lead1.name))
            for crm in lead1:
                res['deal_stage'] = crm.stage_id.id
                res['domain'] = crm.email_from
                res['user_id'] = crm.user_id.id
                res['deal_owner'] = crm.user_id.name 
                res['product_id'] = [(6, 0, crm.product.ids)] 
                res['product_category'] = [(6, 0, crm.product_category.ids)]   
        
    
        return res


class ResUsersInherited(models.Model):
    _inherit = 'res.users'

    status = fields.Selection([
        ('online', 'Online'),
        ('offline', 'Offline')
    ], string="Status", compute="_compute_user_online", store=False, readonly=True)

    setaway = fields.Boolean(string="Available")

    @api.depends_context('uid')
    def _compute_user_online(self):
        presence_env = self.env['bus.presence']
        timeout_minutes = 5  # Consider user offline if no presence update in last 5 minutes
        timeout_threshold = datetime.now() - timedelta(minutes=timeout_minutes)

        for user in self:
            presence = presence_env.search([('user_id', '=', user.id)], limit=1)
            _logger.debug(
                f"User {user.id}: Presence={presence}, Status={presence.status if presence else 'No record'}, Last Presence={presence.last_presence if presence else 'None'}")

            if presence and presence.status == 'online' and presence.last_presence >= timeout_threshold:
                user.status = 'online'
            else:
                user.status = 'offline'

    @api.model
    def cleanup_stale_presence(self):
        """Clean up stale bus.presence records."""
        timeout_minutes = 5
        threshold = datetime.now() - timedelta(minutes=timeout_minutes)
        stale_presences = self.env['bus.presence'].search(
            [('last_presence', '<', threshold), ('status', '=', 'online')])
        if stale_presences:
            _logger.info(f"Cleaning up {len(stale_presences)} stale presence records")
            stale_presences.write({'status': 'offline'})

class EmployeeInherited(models.Model):
    _inherit = 'hr.employee'
    
    online_stat = fields.Selection([('online_online', 'Online'), ('online_setaway', 'Set Away')], string = "Online Status")

    certification = fields.Char('Certification')

    def online_statuss(self):
        for rec in self:
            rec['online_stat'] = 'online_online'
            rec['show_hr_icon_display'] = True
    def online_statusss(self):
        for rec in self:
            rec['online_stat'] = 'online_setaway'


class MailingContactInherited(models.Model):
    _inherit = 'mailing.contact'
    
    company = fields.Many2one('res.partner',string="Company Name", domain=[('is_company', '=', True)])

    def mailing_open_wizard(self):
        
        view = self.env.ref('ocean_fields_ext.mailing_wizard_form')
        # us = []
        # for user in self:
        #     us.append(user.id)
        #     ticket_ids = [(6, 0, us)]
        # raise UserError(self)
        return {
            'name': 'Mailing Wizard',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': 'mailing.wizard',
            'target': 'new',
            # 'context': {'default_ticket_ids': ids },
        }