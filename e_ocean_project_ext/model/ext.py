from odoo import fields, models, api, _
from datetime import datetime,timedelta,date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError



class ApprovalInherited(models.Model):
    _inherit = "approval.request"


    position = fields.Char(string="Position")
    date_required = fields.Date(string="Date Required")
    position_rank = fields.Selection([('Senior Management','Senior Management'),('Middle Management','Middle Management'),('Other','Other')],string="Position Rank")
    direct_reportees = fields.Char(string="Direct Reprotees")
    indirect_reportees = fields.Char(string="Indirect Reprotees")
    position_summary = fields.Text(string="Position Summary")
    qualification = fields.Char(string="Qualification")
    minimum_education = fields.Char(string="Minimum Education")
    experience = fields.Char(string="Experience")
    budget = fields.Char(string="Budget")
    non_budget = fields.Char(string="Non-Budget")
    job_description = fields.Text(string="Job Description")
    age = fields.Date(string="Age")
    gender = fields.Selection([('Male','Male'),('Female','Female'),('Other','Other')],string="Gender")
    years_of_experience = fields.Char(string="Years of Industry Experience")
    package = fields.Char(string="Gross Compensation Package")
    # department_approver = fields.Many2one('res.users',string="Department Head")
    # department_approver_date = fields.Date(string="Date")
    # hr_approver = fields.Many2one('res.users',string="Manager HR")
    # hr_approver_date = fields.Date(string="Date")
    # ceo_approver = fields.Many2one('res.users',string="CEO")
    # ceo_approver_date = fields.Date(string="Date")

    def action_approve(self, *args, **kwargs):
        res = super(ApprovalInherited, self).action_approve(*args, **kwargs)
        for rec in self:
            if rec.request_owner_id:
                message = f"Your approval request {rec.name} has been approved."
                rec.message_post(
                    body=message,
                    partner_ids=[rec.request_owner_id.partner_id.id],
                    subtype_xmlid="mail.mt_comment"
                )
        return res
 
        



class ProjectInherited(models.Model):
    _inherit = "project.task"

    # Incident Management
    # stage1
    incident_date = fields.Datetime(string="Date & Time of Incident",tracking=True)
    contact_name = fields.Char(string="Name & Contact of Reporter",tracking=True)
    incident_location = fields.Char(string="Incident Location",tracking=True)
    incident_category = fields.Selection([('technical','Technical'),('administrative','Administrative'),('security','Security')],string="Incident Category",tracking=True)
    incident_description = fields.Text(string="Incident Description",tracking=True)
    # stage2
    incident_category_2 = fields.Selection([('weakness ','Weakness '),('event','Event')],string="Incident Category",tracking=True)
    incident_no = fields.Char(string="Incident Number",tracking=True)
    approver_id = fields.Many2many('res.users','company_id',string="Assigned for Resolution to",tracking=True)
    closure_date = fields.Date(string="Proposed Closure Date",tracking=True)
    # stage3
    root_cause = fields.Text(string="Root Cause",tracking=True)
    corrective_action = fields.Text(string="Corrective Action",tracking=True)
    evidences = fields.Text(string="Evidences",tracking=True)
    user_name_resolver = fields.Many2one('res.users',string="Name Of Resolver",tracking=True, readonly=True)
    # user_signature = fields.Binary(string="Signature",tracking=True)
    resolution_date = fields.Date(string="Resolution Date",tracking=True)
    date1 = fields.Date(string="Date",tracking=True)
    # stage4
    incident_feedback = fields.Selection([('satisfied  ','Satisfied'),('not satisfied','Not Satisfied')],string="Incident Reporter’s Feedback",tracking=True)
    comments = fields.Text(string="Comments",tracking=True)
    date2 = fields.Date(string="Date",tracking=True)
    user_reporter = fields.Char(string="Name Of Reporter",tracking=True)
    # user_signature2 = fields.Binary(string="Signature",tracking=True)
    # stage5
    incident_status = fields.Selection([('closed','Closed'),('not closed','Not Closed')],string="Incident Status",tracking=True)
    comments2 = fields.Text(string="Comments",tracking=True)
    user_name3 = fields.Many2one('res.users',string="Name Of Incident Manager",tracking=True)
    # user_signature3 = fields.Binary(string="Signature",tracking=True)
    date3 = fields.Date(string="Date",tracking=True)

    # Change Management
    # stage1
    cmf_no = fields.Char(string="CMF #",tracking=True)
    readonly = fields.Boolean(string="Readonly")
    change_instance = fields.Selection([('scheduled','Scheduled'),('urgent','Urgent')],string="Change Instance",tracking=True)
    change_type = fields.Selection([('major','Major'),('minor','Minor')],string="Change Type",tracking=True)
    change_description = fields.Text(string="Change Description",tracking=True)
    rationale_for_change = fields.Text(string="Rationale for Change",tracking=True)
    remarks = fields.Text(string="Remarks",tracking=True)
    change_category = fields.Selection([('incident','Incident'),('non-conformance','Non-Conformance'),('preventive action','Preventive Action'),('new requirement','New Requirement')],string="Category of Change",tracking=True)
    # initiator = fields.Many2one('res.users',string="Initiator",tracking=True)
    # origination_date = fields.Date(string="Proposed Closure Date",tracking=True)
    description3 = fields.Text(string="Description",tracking=True)
    # stage2
    related_risk = fields.Text(string="Related Risk",tracking=True)
    impact = fields.Text(string="Impact",tracking=True)
    contingency_plan = fields.Text(string="Risk Mitigation / Contingency Plan",tracking=True)
    # stage3
    approve_by1 = fields.Many2one('res.users',string="Approve By Eocean",tracking=True)
    approve_by11 = fields.Many2one('res.users',string="Approve By Interkey",tracking=True)
    department = fields.Char(string="Department",tracking=True)
    user_signature4 = fields.Binary(string="Signature",tracking=True)
    date4 = fields.Date(string="Date",tracking=True)
    date41 = fields.Date(string="Date",tracking=True)
    # stage4
    implementer = fields.Many2one('res.users',string="Assigned to Implementer",tracking=True)
    second_implementer_name = fields.Many2one('res.users',string="2nd Implementer’s Name",tracking=True)
    backup_procedure = fields.Text(string="Backup Procedure",tracking=True)
    deployment_procedure = fields.Text(string="Deployment Procedure",tracking=True)
    implementation_lead = fields.Text(string="Implementation Lead",tracking=True)
    deployment_notes = fields.Text(string="Deployment Notes",tracking=True)
    # stage5
    resolved_date = fields.Datetime(string="Resolved Date",tracking=True)
    closed_date = fields.Datetime(string="Closed Date",tracking=True)
    implementation_lead_name = fields.Text(string="Implementation Lead Name",tracking=True)
    Initiator_name = fields.Many2one('res.users',string="Initiator’s Name",tracking=True)
    initiator_signature = fields.Binary(string="Signature",tracking=True)
    


    # Access Management
    # stage1
    department_id = fields.Many2one('hr.department',string="Department",tracking=True)
    acm_no = fields.Char(string="ACM #",tracking=True)
    agreement = fields.Boolean(string="Agreement Checkbox")
    comments3 = fields.Text(string="Comments",tracking=True)
    approved_users = fields.Many2many('res.users','company_id', string="Approved Users")
    is_approved = fields.Boolean(string="Fully Approved", compute="_compute_approval", store=True)
    access_type = fields.Selection([('temporary','Temporary'),('permanent','Permanent')],string="Access Type",tracking=True)
    time_period  = fields.Char(string="Time Period",tracking=True)
    role  = fields.Text(string="Role",tracking=True)
    type_of_engagement  = fields.Selection([('Eocean','Eocean'),('Contractor','Contractor')],string="TYPE OF ENGAGEMENT WITH THE CLIENT",tracking=True)
    # stage3
    comments4 = fields.Text(string="Comments",tracking=True)
    # stage4
    approver_name = fields.Many2one('res.users',string="Approver By Eocean",tracking=True)
    approver_name1 = fields.Many2one('res.users',string="Approver By InterKey",tracking=True)
    cto_signature = fields.Binary(string="CTO Signature",tracking=True)
    date5 = fields.Date(string="Date",tracking=True)
    date51 = fields.Date(string="Date",tracking=True)

    # VPN And Ip Whiitelisting
    company_name = fields.Char(string="Company",tracking=True)
    type_of_access = fields.Selection([('temporary','Temporary'),('permanent','Permanent')],string="Access Type",tracking=True)
    sales_approver = fields.Many2one('res.users',string="Approver",tracking=True, domain=[("groups_id", "in", [14])])
    public_ip1 = fields.Text(string="Public IP",tracking=True)
    private_ip1 = fields.Text(string="Private IP",tracking=True)

    first_approval = fields.Boolean(string="First Approval")
    second_approval = fields.Boolean(string="Second Approval")


    # CHECKING BOTH THE FIELDS THAT IN BOTH FIELDS ALL USERS ARE SAME OR NOT IF SAME THEN TRUE
    @api.depends('approved_users', 'user_ids')
    def _compute_approval(self):
        for rec in self:
            rec.is_approved = set(rec.approved_users.ids) >= set(rec.user_ids.ids)

    # APPENDING IN THE APPROVED_USERS FIELDS ONLY THOSE WHO ARE IN USER_IDS ONLY THOSE CAN CLICK THAT BUTTON
    def resolved(self):
        for rec in self:
            if rec.user_ids and rec.project_id.id in (32,57):
                user = self.env.user


                if user.id not in rec.user_ids.ids:
                    raise UserError(_("You are not in the approval list!"))

                if user.id in rec.approved_users.ids:
                    raise UserError(_("You have already approved this."))

                rec.approved_users = [(4, user.id)]  

                if rec.is_approved:
                    rec._finalize_approval()

    # CONVERTING STAGE TO RESOLVED
    def _finalize_approval(self):
        for rec in self:
            if rec.project_id.id == 32:
                rec.write({'stage_id': 361}) 
            if rec.project_id.id == 57:
                rec.write({'stage_id': 606}) 

    def in_progress(self):
        for rec in self:
            required_fields_filled = all([
                rec.incident_date,
                rec.contact_name,
                rec.incident_location,
                rec.incident_category,
                rec.user_name_resolver,
                rec.incident_category_2,
                rec.incident_no,
                rec.approver_id,
                rec.closure_date,
                rec.description3,
            ])
            
            if rec.project_id.id == 34:
                if required_fields_filled:
                    rec.write({'stage_id': 371})
                else:
                    raise UserError("All the required fields have not been filled.")
            
            elif rec.project_id.id == 58:
                if required_fields_filled:
                    rec.write({'stage_id': 611})
                else:
                    raise UserError("All the required fields have not been filled.")
            
            elif rec.project_id.id == 32:
                rec.write({'stage_id': 359})

            elif rec.project_id.id == 33:
                rec.write({'stage_id': 365})

            elif rec.project_id.id == 59:
                rec.write({'stage_id': 638})

            elif rec.project_id.id == 57:
                rec.write({'stage_id': 604})




    def pending_at_client(self):
        for rec in self:
            if rec.project_id.id == 38:
                rec.write({'stage_id': 453})  
            if rec.project_id.id == 39:
                rec.write({'stage_id': 458})  

    def pending_at_eocean(self):
        for rec in self:
            if rec.project_id.id == 38:
                rec.write({'stage_id': 454})  
            if rec.project_id.id == 39:
                rec.write({'stage_id': 459})  
    def done1(self):
        for rec in self:
            if rec.project_id.id == 38:
                rec.write({'stage_id': 455})  
            if rec.project_id.id == 39:
                rec.write({'stage_id': 460})  
    def rejected(self):
        for rec in self:
            if rec.project_id.id == 38:
                rec.write({'stage_id': 456})  
            if rec.project_id.id == 39:
                rec.write({'stage_id': 461})  

    def on_hold(self):
        for rec in self:
            if rec.project_id.id == 34:
                rec.write({'stage_id': 372})  
            if rec.project_id.id == 32:
                rec.write({'stage_id': 360})  
            if rec.project_id.id == 33:
                rec.write({'stage_id': 366})
            if rec.project_id.id == 59:
                rec.write({'stage_id': 639})
            if rec.project_id.id == 58:
                rec.write({'stage_id': 612})  
            if rec.project_id.id == 57:
                rec.write({'stage_id': 605})  

    def revoke_access(self):
        for rec in self:
            if rec.project_id.id == 32:
                rec.write({'stage_id': 440}) 
            if rec.project_id.id == 57:
                rec.write({'stage_id': 607}) 

    def resolved1(self):
        for rec in self:
            if rec.project_id.id == 33:
                rec.write({'stage_id': 367})  
            if rec.project_id.id == 59:
                rec.write({'stage_id': 640})  

    def closed(self):
        for rec in self:
            if rec.project_id.id == 34:
                rec.write({'stage_id': 374})  
            if rec.project_id.id == 32:
                rec.write({'stage_id': 362})  
            if rec.project_id.id == 33:
                rec.write({'stage_id': 368})
            if rec.project_id.id == 59:
                rec.write({'stage_id': 641})
            if rec.project_id.id == 58:
                rec.write({'stage_id': 614})  
            if rec.project_id.id == 57:
                rec.write({'stage_id': 608})  

    def cancelled(self):
        for rec in self:
            if rec.project_id.id == 34:
                rec.write({'stage_id': 375})  
            if rec.project_id.id == 32:
                rec.write({'stage_id': 363})  
            if rec.project_id.id == 33:
                rec.write({'stage_id': 369})
            if rec.project_id.id == 59:
                rec.write({'stage_id': 642})
            if rec.project_id.id == 58:
                rec.write({'stage_id': 615})  
            if rec.project_id.id == 57:
                rec.write({'stage_id': 609})  

    def un_cancelled(self):
        for rec in self:
            if rec.project_id.id == 34:
                rec.write({'stage_id': 370,
                           'first_approval' : False,
                           'second_approval' : False
                           
                           })  
            if rec.project_id.id == 32:
                rec.write({'stage_id': 358,
                           'approved_users' : False,
                           'first_approval' : False,
                           'second_approval' : False
                           
                           })  
            if rec.project_id.id == 33:
                rec.write({'stage_id': 364,
                           'first_approval' : False,
                           'second_approval' : False
                           
                           })
            if rec.project_id.id == 59:
                rec.write({'stage_id': 637,
                           'first_approval' : False,
                           'second_approval' : False
                           })
            if rec.project_id.id == 38:
                rec.write({'stage_id': 462})  
            if rec.project_id.id == 39:
                rec.write({'stage_id': 463})  
            if rec.project_id.id == 57:
                rec.write({'stage_id': 603,
                           'approved_users': False,
                           'first_approval' : False,
                           'second_approval' : False
                           })  
            if rec.project_id.id == 58:
                rec.write({'stage_id': 610,
                           'first_approval' : False,
                           'second_approval' : False
                           
                           }) 


            


    def approve_by_second(self):
        for rec in self:
            if rec.project_id.id == 58:
                user = self.env.user
                if user.id in (75,79,76):
                    rec.second_approval = True
                    rec.message_post(
                        body=f"Approval given by {self.env.user.name}.",
                        partner_ids=rec.message_partner_ids.ids,
                        subtype_xmlid="mail.mt_comment"
                    )
                    if rec.first_approval and rec.second_approval:
                        rec.stage_id = 613
                        # rec.user_ids = [(4, 104),(4, 205)]
                        message = f"Task {rec.name} has been Approved."
                    
                        rec.message_post(
                            body=message,
                            partner_ids=rec.message_partner_ids.ids,
                            subtype_xmlid="mail.mt_comment"
                        )
                    # , (4, 567)
                else:
                    raise UserError("You are not the Approver")
            elif rec.project_id.id == 59:
                user = self.env.user
                if user.id in (75,79) and rec.cmf_no and rec.user_ids and rec.change_instance and rec.change_type and rec.rationale_for_change and rec.change_category and rec.description3 and rec.related_risk and rec.impact and rec.contingency_plan and rec.implementer and rec.second_implementer_name and rec.backup_procedure and rec.deployment_notes and rec.deployment_procedure and rec.implementation_lead:
                    rec.second_approval = True
                    rec.approve_by11 = user.id
                    rec.date41 = date.today()
                    rec.message_post(
                        body=f"Approval given by {self.env.user.name}.",
                        partner_ids=rec.message_partner_ids.ids,
                        subtype_xmlid="mail.mt_comment"
                    )
                    if rec.first_approval and rec.second_approval:
                        rec.stage_id = 638
                        rec.department = user.employee_id.department_id.name
                        message = f"Task {rec.name} has been Approved."
                    
                        rec.message_post(
                            body=message,
                            partner_ids=rec.message_partner_ids.ids,
                            subtype_xmlid="mail.mt_comment"
                        )
                else:
                    raise UserError("You are not the Approver Or the All the fields havent been filled")
            elif rec.project_id.id == 57:
                user = self.env.user
                if user.id in (75,79,76) and rec.department_id and rec.user_ids and rec.acm_no and rec.access_type and rec.role and rec.type_of_engagement and rec.comments3 and rec.description3:
                    rec.second_approval = True
                    rec.approver_name1 = user.id
                    rec.date51 = date.today()
                    rec.message_post(
                        body=f"Approval given by {self.env.user.name}.",
                        partner_ids=rec.message_partner_ids.ids,
                        subtype_xmlid="mail.mt_comment"
                    )
                    if rec.first_approval and rec.second_approval:
                        rec.stage_id = 604
                        message = f"Task {rec.name} has been Approved."
                    
                        rec.message_post(
                            body=message,
                            partner_ids=rec.message_partner_ids.ids,
                            subtype_xmlid="mail.mt_comment"
                        )
                else:
                    raise UserError("You are not the Approver Or the All the fields havent been filled")
            
                


    def approve_by(self):
        for rec in self:
            if rec.project_id.id == 34:
                user = self.env.user
                if user.id in (147,76,2):
                    rec.stage_id = 373
                    rec.user_ids = [(4, 104),(4, 205)]
                    message = f"Task {rec.name} has been Approved."
                
                    rec.message_post(
                        body=message,
                        partner_ids=rec.message_partner_ids.ids,
                        subtype_xmlid="mail.mt_comment"
                    )
                    # , (4, 567)
                else:
                    raise UserError("You are not the Approver")
            elif rec.project_id.id == 58:
                user = self.env.user
                if user.id in (147,76,2):
                    rec.first_approval = True
                    rec.message_post(
                        body=f"Approval given by {self.env.user.name}.",
                        partner_ids=rec.message_partner_ids.ids,
                        subtype_xmlid="mail.mt_comment"
                    )
                    
                    if rec.first_approval and rec.second_approval:
                        rec.stage_id = 613
                        # rec.user_ids = [(4, 104),(4, 205)]
                        message = f"Task {rec.name} has been Approved."
                    
                        rec.message_post(
                            body=message,
                            partner_ids=rec.message_partner_ids.ids,
                            subtype_xmlid="mail.mt_comment"
                        )
                    # , (4, 567)
                else:
                    raise UserError("You are not the Approver")
            elif rec.project_id.id == 33:
                user = self.env.user
                if user.id in (147,76) and rec.cmf_no and rec.user_ids and rec.change_instance and rec.change_type and rec.rationale_for_change and rec.change_category and rec.description3 and rec.related_risk and rec.impact and rec.contingency_plan and rec.implementer and rec.second_implementer_name and rec.backup_procedure and rec.deployment_notes and rec.deployment_procedure and rec.implementation_lead:
                    rec.stage_id = 365
                    rec.approve_by1 = user.id
                    rec.date4 = date.today()
                    rec.department = user.employee_id.department_id.name
                    message = f"Task {rec.name} has been Approved."
                
                    rec.message_post(
                        body=message,
                        partner_ids=rec.message_partner_ids.ids,
                        subtype_xmlid="mail.mt_comment"
                    )
                else:
                    raise UserError("You are not the Approver Or the All the fields havent been filled")
            elif rec.project_id.id == 59:
                user = self.env.user
                if user.id in (147,76,2) and rec.cmf_no and rec.user_ids and rec.change_instance and rec.change_type and rec.rationale_for_change and rec.change_category and rec.description3 and rec.related_risk and rec.impact and rec.contingency_plan and rec.implementer and rec.second_implementer_name and rec.backup_procedure and rec.deployment_notes and rec.deployment_procedure and rec.implementation_lead:
                    rec.first_approval = True
                    rec.approve_by1 = user.id
                    rec.date4 = date.today()
                    rec.message_post(
                        body=f"Approval given by {self.env.user.name}.",
                        partner_ids=rec.message_partner_ids.ids,
                        subtype_xmlid="mail.mt_comment"
                    )
                    if rec.first_approval and rec.second_approval:
                        rec.stage_id = 638
                        rec.department = user.employee_id.department_id.name
                        message = f"Task {rec.name} has been Approved."
                    
                        rec.message_post(
                            body=message,
                            partner_ids=rec.message_partner_ids.ids,
                            subtype_xmlid="mail.mt_comment"
                        )
                else:
                    raise UserError("You are not the Approver Or the All the fields havent been filled")
            elif rec.project_id.id == 32:
                user = self.env.user
                if user.id in (147,76,2) and rec.department_id and rec.user_ids and rec.acm_no and rec.access_type and rec.role and rec.type_of_engagement and rec.comments3 and rec.description3:
                    rec.stage_id = 359
                    rec.approver_name = user.id
                    rec.date5 = date.today()
                    message = f"Task {rec.name} has been Approved."
                
                    rec.message_post(
                        body=message,
                        partner_ids=rec.message_partner_ids.ids,
                        subtype_xmlid="mail.mt_comment"
                    )
                else:
                    raise UserError("You are not the Approver Or the All the fields havent been filled")
            elif rec.project_id.id == 57:
                user = self.env.user
                if user.id in (147,76,2) and rec.department_id and rec.user_ids and rec.acm_no and rec.access_type and rec.role and rec.type_of_engagement and rec.comments3 and rec.description3:
                    rec.first_approval = True
                    rec.approver_name = user.id
                    rec.date5 = date.today()
                    rec.message_post(
                        body=f"Approval given by {self.env.user.name}.",
                        partner_ids=rec.message_partner_ids.ids,
                        subtype_xmlid="mail.mt_comment"
                    )
                    if rec.first_approval and rec.second_approval:
                        rec.stage_id = 604
                        message = f"Task {rec.name} has been Approved."
                    
                        rec.message_post(
                            body=message,
                            partner_ids=rec.message_partner_ids.ids,
                            subtype_xmlid="mail.mt_comment"
                        )
                else:
                    raise UserError("You are not the Approver Or the All the fields havent been filled")
            elif rec.project_id.id ==39:
                user = self.env.user
                if user.id in (147,76,2):
                    rec.stage_id = 457
                    message = f"Task {rec.name} has been Approved."
                
                    rec.message_post(
                        body=message,
                        partner_ids=rec.message_partner_ids.ids,
                        subtype_xmlid="mail.mt_comment"
                    )
                else:
                    raise UserError("You are not the Approver")
            elif rec.project_id.id ==38:
                user = self.env.user
                if user.id in (147,76,2):
                    rec.stage_id = 452
                    message = f"Task {rec.name} has been Approved."
                
                    rec.message_post(
                        body=message,
                        partner_ids=rec.message_partner_ids.ids,
                        subtype_xmlid="mail.mt_comment"
                    )


                else:
                    raise UserError("You are not the Approver")


    @api.model
    def create(self, vals):
        if 'project_id' in vals:  
            if vals['project_id'] == 34 and not vals.get('incident_no'):
                vals['incident_no'] = self.env['ir.sequence'].next_by_code('inc.man') or '/'
            elif vals['project_id'] == 33 and not vals.get('cmf_no'):
                vals['cmf_no'] = self.env['ir.sequence'].next_by_code('cha.man') or '/'
            elif vals['project_id'] == 32 and not vals.get('acm_no'):
                vals['acm_no'] = self.env['ir.sequence'].next_by_code('acc.man') or '/'
            elif vals['project_id'] == 59 and not vals.get('cmf_no'):
                vals['cmf_no'] = self.env['ir.sequence'].next_by_code('cha.man1') or '/'
            elif vals['project_id'] == 57 and not vals.get('acm_no'):
                vals['acm_no'] = self.env['ir.sequence'].next_by_code('acc.man1') or '/'
            if vals['project_id'] == 58 and not vals.get('incident_no'):
                vals['incident_no'] = self.env['ir.sequence'].next_by_code('inc.man1') or '/'
        
        return super(ProjectInherited, self).create(vals)

    

    def write(self, vals):
        res = super(ProjectInherited, self).write(vals)  
        # project_id = vals.get('project_id')
        # raise UserError(str(vals.get('project_id')))
        # if project_id == 33:
        if vals.get('approver_id'):
            for rec in self:
                message = f"You have been assigned as the approver for Task {rec.name}."
                
                rec.message_post(
                    body=message,
                    partner_ids=rec.approver_id.ids,
                    subtype_xmlid="mail.mt_comment"
                )

                activity_type = rec.env.ref("mail.mail_activity_data_todo")
                for approver in rec.approver_id:
                    rec.activity_schedule(
                        activity_type_id=activity_type.id,
                        summary="Approval Required",
                        user_id=approver.id,  
                        note=message
                    )
        if vals.get('stage_id') == 373:  
            self['user_name_resolver'] = self.env.user.id
        if vals.get('stage_id') == 367: 
            for rec in self: 
                message = f"Task {rec.name} has been resolved, kindly closed it."
                    
                rec.message_post(
                    body=message,
                    partner_ids=[rec.create_uid.id],
                    subtype_xmlid="mail.mt_comment"
                )


        # if project_id == 34:
        if vals.get('implementer'):
            for rec in self:
                message = f"You have been assigned as the Implementor for Task {rec.name}."
                partner_id = rec.implementer.partner_id.id if rec.implementer and rec.implementer.partner_id else False
                if partner_id:
                    rec.message_post(
                        body=message,
                        # partner_ids=[rec.implementer.id],
                        partner_ids=[partner_id],
                        subtype_xmlid="mail.mt_comment"
                    )

                activity_type = rec.env.ref("mail.mail_activity_data_todo")
                for approver in rec.implementer:
                    rec.activity_schedule(
                        activity_type_id=activity_type.id,
                        summary="Approval Required",
                        user_id=approver.id,  
                        note=message
                    )

        elif vals.get('second_implementer_name'):
            for rec in self:
                message = f"You have been assigned as the 2nd Implementor for Task {rec.name}."
                partner_id = rec.second_implementer_name.partner_id.id if rec.second_implementer_name and rec.second_implementer_name.partner_id else False
                if partner_id:
                    rec.message_post(
                        body=message,
                        # partner_ids=[rec.second_implementer_name.id],
                        partner_ids=[partner_id],
                        subtype_xmlid="mail.mt_comment"
                    )

                activity_type = rec.env.ref("mail.mail_activity_data_todo")
                for approver in rec.second_implementer_name:
                    rec.activity_schedule(
                        activity_type_id=activity_type.id,
                        summary="Approval Required",
                        user_id=approver.id,  
                        note=message
                    )
        if vals.get('sales_approver'):
            for rec in self:
                message = f"You have been assigned as the Approver for Task {rec.name}."
                
                rec.message_post(
                    body=message,
                    partner_ids=[rec.sales_approver.id],
                    subtype_xmlid="mail.mt_comment"
                )

                activity_type = rec.env.ref("mail.mail_activity_data_todo")
                for approver in rec.sales_approver:
                    rec.activity_schedule(
                        activity_type_id=activity_type.id,
                        summary="Approval Required",
                        user_id=approver.id,  
                        note=message
                    )
        if vals.get('stage_id') in (367,640):  
            self['resolved_date'] = fields.Datetime.now()
        elif vals.get('stage_id') in (369,641):  
            self['implementation_lead_name'] = self.env.user.name
            self['closed_date'] = fields.Datetime.now()
            
            
        return res  
    



