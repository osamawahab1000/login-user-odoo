from odoo import fields, models, api, _
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError



class KPISample(models.Model):
    _name = "kpi.sample"
    _rec_name='employee_id'

    employee_id = fields.Many2one('hr.employee',string="Employee")
    job_description = fields.Many2one('hr.department',string="Department",compute="get_department")
    job_position = fields.Many2one('hr.job',string="Job Position" ,compute="get_department")
    parent_department = fields.Many2one('hr.department',string="Parent Department",compute="get_department")
    report_to = fields.Many2one('res.users',string="Report To")
    location = fields.Char(string='Location')
    note1 = fields.Html(string="Note")
    kpi_sample_line_ids = fields.One2many('kpi.sample.line', 'kpi_id', string="KPIS")

    @api.depends('employee_id')
    def get_department(self):
        for rec in self:
            rec['job_description'] = False
            rec['job_position'] = False
            rec['parent_department'] = False
            if rec.employee_id:
                rec['job_description'] = rec.employee_id.department_id.id
                rec['job_position'] = rec.employee_id.job_id.id
                if rec.employee_id.department_id.parent_id:
                    rec['parent_department'] = rec.employee_id.department_id.parent_id.id



class KPISampleLine(models.Model):
    _name = "kpi.sample.line"

    kpi_id = fields.Many2one('kpi.sample', string="KPIS", ondelete="cascade")
    kpi = fields.Char(string="KPI")
    target = fields.Char(string="Target")
    actual_performance = fields.Char(string="Actual Performance")
    remarks = fields.Char(string="Remarks")

job_position = {
    'AM Accounts/Finance': 436,
    'AM Taxation': 438,
    'Account Receivables Associate': 422,
    'Accounts Executive': 413,
    'Accounts Officer': 385,
    'Admin': 448,
    'Animator': 421,
    'Assistant Manager Sales': 390,
    'Assistant Operation manager': 419,
    'Associate Business Analyst': 432,
    'Associate Manager Digital': 434,
    'CEO': 376,
    'CFO': 433,
    'CISO': 370,
    'CSE': 417,
    'CSR': 362,
    'CTO': 441,
    'Call center agent': 379,
    'Campaign Executive': 375,
    'Campaign Manager': 363,
    'Chairman': 404,
    'Chief Business officer': 431,
    'Cleaner': 365,
    'Compliance Executive': 415,
    'Consultant': 429,
    'Content Writer': 427,
    'Customer Service Execuive': 443,
    'Customer Service Executive': 387,
    'Customer Success Executive': 372,
    'Customer Success Team Lead': 391,
    'Customer Success manager': 399,
    'Data Engineer': 395,
    'DevOps Engineer': 380,
    'Developer': 407,
    'Devops engineer': 447,
    'Digital Marketing Specialist': 389,
    'Director of Products': 425,
    'Driver': 394,
    'East, Middle East Accounts Executive': 423,
    'GENERIC TEST JP': 452,
    'Google Workspace Administrator': 386,
    'Graphic Designer': 364,
    'HR Generalist': 430,
    'Head Of Communications': 396,
    'Head Of HR & Admin': 426,
    'Head of Customer Success': 437,
    'Head of Digital': 409,
    'Head of Operations': 424,
    'Head of Operations - North': 371,
    'Human Resources Officer': 449,
    'IT coordinator': 420,
    'Jr. Legal Officer': 444,
    'Junior ISO': 405,
    'Junior Software Engineer Full stack': 401,
    'Lead Creative Designer': 388,
    'Lead HRBP': 398,
    'Legal Counsel': 393,
    'MTO': 406,
    'MTO-HR': 414,
    'Manager CE': 275,
    'Manager Customer Services': 368,
    'Manager Infrastructure': 384,
    'Manager Sales': 408,
    'Manager Software Development': 416,
    'NOC Engineer': 381,
    'Network Engineer': 411,
    'Network Manager': 383,
    'Network support engineer': 392,
    'Office Boy': 366,
    'Office Runner': 410,
    'Principal Software Engineer': 400,
    'Product Manager': 367,
    'Program Manager': 418,
    'Project Coordinater': 361,
    'Project Manager': 382,
    'QA': 451,
    'Resident Engineer HBL': 402,
    'SQA Engineer': 412,
    'SQA Manager': 440,
    'Sales Manager': 397,
    'Senior IT Coordinator': 369,
    'Senior Software Engineer': 377,
    'Senior Technical Recruiter': 450,
    'Software Engineer': 378,
    'Solution Delivery Associate': 403,
    'Solutions Delivery Manager': 439,
    'Sr HR & Admin Executive': 435,
    'Sr PHP Developer': 374,
    'Sr SQA Engineer': 373,
    'Talent Acquisition Specialist': 428,
    'Technician': 442,
    'VP Growth': 445
}


class EmployeesInherited(models.Model):
    _inherit = "hr.employee"

    employee_id1 = fields.Char(string="Employee ID")
    last_day_of_service = fields.Char(string="Last Day Of Service")
    supervisor_name = fields.Many2one('res.users',string="Supervisor Name")
    type_of_separation = fields.Selection([('Resignation','Resignation'),('Termination','Termination')],string="Type Of Separation")
    # Immediate Supervisor
    handover = fields.Boolean(string="Tasks completed and project handover done")
    data_clearance = fields.Boolean(string="Data clearance (Team Lead/Project Manager sign-off)")
    comment1 = fields.Text(string="Comment")
    approved_by1 = fields.Many2one('res.users',string="Approved By",compute="get_approved_by")
    date1 = fields.Date(string="Date", compute="get_approved_by")
    # IT Department
    laptop = fields.Boolean(string="Laptop bag (with charger & power cable) & other accessories-returned")
    company_phone = fields.Boolean(string="Company phone (if issued) - returned")
    comment2 = fields.Text(string="Comment")
    asset_serial_number = fields.Text(string="Asset/Serial Number")
    approved_by2 = fields.Many2one('res.users',string="Approved By",compute="get_approved_by")
    date2 = fields.Date(string="Date",compute="get_approved_by")
    # Access Revocation Confirmation 
    email_id1 = fields.Boolean(string="Email ID, Google drive, Email Forwarding. Slack, Zoom, Cloud Storage etc. ")
    comment3 = fields.Text(string="Comment")
    approved_by3 = fields.Many2one('res.users',string="Approved By",compute="get_approved_by")
    date3 = fields.Date(string="Date",compute="get_approved_by")
    # Admin Department  
    company_card = fields.Boolean(string="Company ID card & other official cards returned (Compulsory) ")
    drawer_keys = fields.Boolean(string="Drawer Keys")
    company_vehicle = fields.Boolean(string="Company Vehicle")
    company_mobile_phone = fields.Boolean(string="Company Mobile Phone")
    company_sim = fields.Boolean(string="Company SIM card (if issued) - returned")
    company_internet = fields.Boolean(string="Company internet device (if issued) - returned")
    removed_from_group = fields.Boolean(string="Removed from company WhatsApp group(s) ")
    comment4 = fields.Text(string="Comment")
    approved_by4 = fields.Many2one('res.users',string="Approved By",compute="get_approved_by")
    date4 = fields.Date(string="Date",compute="get_approved_by")
    # Finance Department  
    outstanding_advances = fields.Boolean(string="Outstanding advances or liabilities settled ")
    receipt_submitted = fields.Boolean(string="All relevant receipts submitted (if any)")
    outstanding_dues = fields.Boolean(string="Outstanding dues or loans cleared (if applicable)")
    comment5 = fields.Text(string="Comment")
    approved_by5 = fields.Many2one('res.users',string="Approved By",compute="get_approved_by")
    date5 = fields.Date(string="Date",compute="get_approved_by")
    # HR Department  
    benefits_cancelled = fields.Boolean(string="Benefits cancelled (health insurance card, PSO Fuel Card )")
    exit_interview_completed = fields.Boolean(string="Exit interview completed (form submitted)")
    hrms_portal = fields.Boolean(string="HRMS portal access revoked")
    signed_document = fields.Boolean(string="NDA Signed Document ")
    resignation_approved_by_hr = fields.Boolean(string="Resignation approved by HR")
    comment6 = fields.Text(string="Comment")
    approved_by6 = fields.Many2one('res.users',string="Approved By")
    date6 = fields.Date(string="Date",compute="get_approved_by")
    all_clearance_done = fields.Boolean(string="Ready for Offboarding", compute="_compute_clearance_status", store=True)

    # Onboarding fields
    # Departmental onboarding booleans or status fields
    onboarding_admin = fields.Boolean("Admin Notified")
    onboarding_it = fields.Boolean("IT Notified")
    onboarding_hr = fields.Boolean("HR Notified")
    onboarding_finance = fields.Boolean("Finance Notified")
    onboarding_operations = fields.Boolean("Operations Notified")

    # Email trigger users for each department
    admin_user_id = fields.Many2one('res.users', string="Admin Responsible")
    it_user_id = fields.Many2one('res.users', string="IT Responsible")
    hr_user_id = fields.Many2one('res.users', string="HR Responsible")
    finance_user_id = fields.Many2one('res.users', string="Finance Responsible")
    operations_user_id = fields.Many2one('res.users', string="Operations Responsible")

    @api.depends(
        'handover', 'data_clearance',
        'laptop', 'company_phone',
        'email_id1',
        'company_card', 'drawer_keys', 'company_vehicle',
        'company_mobile_phone', 'company_sim', 'company_internet', 'removed_from_group',
        'outstanding_advances', 'receipt_submitted', 'outstanding_dues',
        'benefits_cancelled', 'exit_interview_completed', 'hrms_portal',
        'signed_document', 'resignation_approved_by_hr'
    )
    def _compute_clearance_status(self):
        for rec in self:
            rec.all_clearance_done = all([
                rec.handover,
                rec.data_clearance,
                rec.laptop,
                rec.company_phone,
                rec.email_id1,
                rec.company_card,
                rec.drawer_keys,
                rec.company_vehicle,
                rec.company_mobile_phone,
                rec.company_sim,
                rec.company_internet,
                rec.removed_from_group,
                rec.outstanding_advances,
                rec.receipt_submitted,
                rec.outstanding_dues,
                rec.benefits_cancelled,
                rec.exit_interview_completed,
                rec.hrms_portal,
                rec.signed_document,
                rec.resignation_approved_by_hr,
            ])

    def action_notify_all_onboarding_departments(self):
        departments = [
            ('admin', self.admin_user_id, self.onboarding_admin, 'onboarding_admin', 'onboarding_admin_email_template'),
            ('it', self.it_user_id, self.onboarding_it, 'onboarding_it', 'onboarding_it_email_template'),
            ('hr', self.hr_user_id, self.onboarding_hr, 'onboarding_hr', 'onboarding_hr_email_template'),
            ('finance', self.finance_user_id, self.onboarding_finance, 'onboarding_finance',
             'onboarding_finance_email_template'),
            ('operations', self.operations_user_id, self.onboarding_operations, 'onboarding_operations',
             'onboarding_operations_email_template'),
        ]

        for dept_key, user, notified, field_name, template_xml_id in departments:
            if user and not notified:
                # Send Email
                template = self.env.ref(f'your_module_name.{template_xml_id}', raise_if_not_found=False)
                if template:
                    template.send_mail(self.id, force_send=True)

                # Create Activity
                self.env['mail.activity'].create({
                    'res_model_id': self.env['ir.model']._get_id('hr.employee'),
                    'res_id': self.id,
                    'user_id': user.id,
                    'summary': f"{dept_key.upper()} Onboarding Task",
                    'note': f"Please complete onboarding steps for {self.name}",
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                })

                self[field_name] = True

    def action_offboard_employee(self):
        for rec in self:
            rec.active = False
            rec.message_post(body=_("Employee has been offboarded and archived."))

    def open_departure_wizard(self):
        self.ensure_one()
        return {
            'name': 'Employee Departure',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.departure.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('hr.hr_departure_wizard_view_form').id,
            'target': 'new',
            'context': {
                'default_employee_id': self.id,
            }
        }


    @api.depends('handover','data_clearance','laptop','company_phone','email_id1','company_card','drawer_keys','company_vehicle','company_mobile_phone','company_sim','company_internet','removed_from_group',
                 'outstanding_advances','receipt_submitted','outstanding_dues','benefits_cancelled','exit_interview_completed',
                 'hrms_portal','signed_document','resignation_approved_by_hr')
    def get_approved_by(self):
        for rec in self:
            today = datetime.today().date()

            # Reset all fields first
            rec.approved_by1 = rec.date1 = False
            rec.approved_by2 = rec.date2 = False
            rec.approved_by3 = rec.date3 = False
            rec.approved_by4 = rec.date4 = False
            rec.approved_by5 = rec.date5 = False
            rec.approved_by6 = rec.date6 = False

            if rec.data_clearance and rec.handover:
                rec.approved_by1 = self.env.user.id
                rec.date1 = today

            if rec.company_phone and rec.laptop:
                rec.approved_by2 = self.env.user.id
                rec.date2 = today

            if rec.email_id1:
                rec.approved_by3 = self.env.user.id
                rec.date3 = today

            if rec.company_card and rec.drawer_keys and rec.company_vehicle and rec.company_mobile_phone \
            and rec.company_sim and rec.company_internet and rec.removed_from_group:
                rec.approved_by4 = self.env.user.id
                rec.date4 = today

            if rec.outstanding_advances and rec.receipt_submitted and rec.outstanding_dues:
                rec.approved_by5 = self.env.user.id
                rec.date5 = today

            if rec.benefits_cancelled and rec.exit_interview_completed and rec.hrms_portal \
            and rec.signed_document and rec.resignation_approved_by_hr:
                rec.approved_by6 = self.env.user.id
                rec.date6 = today

class HrDepartureWizard(models.TransientModel):
    _inherit = 'hr.departure.wizard'

    # Assign responsible users per department
    it_user_id = fields.Many2one('res.users', string="IT Department User")
    hr_user_id = fields.Many2one('res.users', string="HR Department User")
    finance_user_id = fields.Many2one('res.users', string="Finance Department User")
    admin_user_id = fields.Many2one('res.users', string="Admin Department User")
    supervisor_user_id = fields.Many2one('res.users', string="Immediate Supervisor")

    def action_register_departure(self):
        if self.departure_reason_id and self.departure_reason_id.name == 'Duplicate Record':
            super().action_register_departure()
        else:
            self.ensure_one()
            employee = self.employee_id
            deadline = self.departure_date or fields.Date.today()

            depart_reason= self.env['hr.departure.reason'].browse(self.departure_reason_id.id) if self.departure_reason_id else None
            if not depart_reason:
                raise UserError(_("Please select a valid departure reason."))
            else:
                if depart_reason.name == 'Fired':
                    employee.type_of_separation = 'Termination'
                else:
                    employee.type_of_separation = 'Resignation'

            employee.last_day_of_service = self.departure_date.strftime('%Y-%m-%d') if self.departure_date else ''

            message_body = _("Employee <b>%s</b> is offboarding. Contract ends on <b>%s</b>.<br/>Please complete the Exit Clearance Form.") % (employee.name, deadline)

            users_to_notify = [
                ('supervisor_user_id', self.supervisor_user_id),
                ('it_user_id', self.it_user_id),
                ('admin_user_id', self.admin_user_id),
                ('finance_user_id', self.finance_user_id),
                ('hr_user_id', self.hr_user_id)
            ]

            for role, user in users_to_notify:
                if user and user.partner_id.email:
                    # Send email
                    self.env['mail.mail'].create({
                        'subject': 'Exit Clearance Required: %s' % employee.name,
                        'email_to': user.partner_id.email,
                        'body_html': message_body,
                    }).send()

                    # Create activity
                    self.env['mail.activity'].create({
                        'res_model_id': self.env['ir.model']._get('hr.employee').id,
                        'res_id': employee.id,
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'summary': 'Exit Clearance Required',
                        'note': message_body,
                        'user_id': user.id,
                        'date_deadline': deadline,
                    })

            employee.message_post(body=_("Exit clearance notifications and activities assigned to department users."))

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Exit Clearance Started'),
                    'message': _('Email & activities sent. Departments must complete clearance before archiving.'),
                    'type': 'success',
                    'sticky': False,
                }
            }

#     name1 = fields.Char(string="Name")
#     position_held = fields.Char(string="Position Held")
#     Department1 = fields.Char(string="Department")

#     @api.depends('name','job_id','department_id')
#     def compute_details(self):
#         for rec in self:
#             if rec.name:
#                 rec['name1'] = rec.name
#             if rec.job_id:
#                 rec['position_held'] = rec.job_id.name


class HRApplicantInherited(models.Model):
    _inherit = "hr.applicant"

    first_interview_date = fields.Datetime(string="First Interview Date", tracking=True)
    first_interview_checkbox = fields.Boolean(string="Checkbox1", compute="first_interview_check")
    first_interview_email_sent = fields.Boolean(string="Email Sent", default=False)
    second_interview_date = fields.Datetime(string="Second Interview Date", tracking=True)
    address = fields.Char(string="Address", tracking=True)
    dob = fields.Date(string="Date Of Birth", tracking=True)
    cnic = fields.Char(string="CNIC#", tracking=True)
    # qualification = fields.Char(string="Qualification", tracking=True)
    years_of_experience = fields.Char(string="Years Of Experience", tracking=True)
    reason = fields.Char(string="Reason to switch from the current company", tracking=True)
    notice_period = fields.Char(string="How long is your notice period at your current organization?", tracking=True)

    communication_skills = fields.Selection([('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],string="Communication Skills", tracking=True)
    comment1 = fields.Text(string="Comment", tracking=True)
    technical_knowledge = fields.Selection([('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],string="Technical Knowledge", tracking=True)
    comment2 = fields.Text(string="Comment", tracking=True)
    problem_solving_ability = fields.Selection([('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],string="Problem Solving Ability", tracking=True)
    comment3 = fields.Text(string="Comment", tracking=True)
    team_fit = fields.Selection([('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],string="Team Fit / Cultural Fit", tracking=True)
    comment4 = fields.Text(string="Comment", tracking=True)
    attitude = fields.Selection([('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],string="Attitude and Professionalism", tracking=True)
    comment5 = fields.Text(string="Comment", tracking=True)
    relevant_experience = fields.Selection([('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],string="Relevant Experience", tracking=True)
    comment6 = fields.Text(string="Comment", tracking=True)

    shortlist = fields.Selection([('Strong Hire','Strong Hire'),('Hire','Hire'),('Move to Next Round','Move to Next Round'),('Hold','Hold')], string="Shortlist", tracking=True)
    reject = fields.Selection([('Strong Reject','Strong Reject'),('Reject','Reject')], string="Reject", tracking=True)
    show_up = fields.Selection([('Show','Show'),('No Show','No Show')], string="Candidate Did Not Show Up", tracking=True)
    additional_comment = fields.Text(string="Additional Comments", tracking=True)
    ex_employer = fields.Many2one('res.partner', string="Ex Employer", tracking=True)
    ex_employer_1 = fields.Char(string="Ex Employer Name", tracking=True)
    ex_employer_email = fields.Char(string="Ex Employer Email", tracking=True)

    @api.depends('first_interview_date')
    def first_interview_check(self):
        for rec in self:
            if rec.first_interview_date:
                interview_date = rec.first_interview_date.date()
                today = datetime.now().date()
                one_day_before = interview_date - timedelta(days=1)
                rec.first_interview_checkbox = (today == one_day_before)
            else:
                rec.first_interview_checkbox = False

    def action_send_email_to_ex_employer(self):
        template = self.env.ref('e_ocean_hr_ext.email_template_reference_check', raise_if_not_found=False)
        if not template:
            raise UserError("Email template not found. Please configure it first.")

        for record in self:
            if not record.ex_employer_email:
                raise UserError("Ex Employer Email is missing.")

            template.email_to = record.ex_employer_email
            template.email_from = self.env.user.email
            template.with_context(default_ex_employer_1=record.ex_employer_1).send_mail(record.id, force_send=True)

    def first_interview_email(self):
        for rec in self:
            if rec.first_interview_checkbox and not rec.first_interview_email_sent:
                template = self.env['mail.template'].search([('id', '=', 80)], limit=1)
                if template:
                    email = str(rec.email_from).split('<')[1].split('>')[0] if '<' in rec.email_from else rec.email_from
                    email_values = {
                        'email_to': email,
                        'subject': "First Interview",
                    }
                    template.send_mail(rec.id, force_send=True, email_values=email_values)
                    rec.first_interview_email_sent = True


    # @api.model
    # def scheduled_first_interview_email(self):
    #     applicants = self.env['hr.applicant'].search([
    #         ('first_interview_checkbox', '=', True),
    #         ('first_interview_email_sent', '=', False),
    #         ('first_interview_date', '!=', False),
    #     ])
    #     for applicant in applicants:
    #         applicant.first_interview_email()



    def trigger_applicant_based_on_job(self):
        for rec in self:
            for job_name, job_id in job_position.items():
                if job_name.lower() == rec.name.lower(): 
                    rec['job_id'] = job_id
                    # existing_applicant = self.env['hr.applicant'].search([
                    #     ('name', '=', rec.name),
                    #     ('partner_name', '=', rec.partner_name),
                    #     ('email_from', '=', rec.email_from),
                    #     ('job_id', '=', job_id)
                    # ], limit=1) 
                    # if not existing_applicant:
                    #     new_applicant = self.env['hr.applicant'].create({
                    #         'name': rec.name,
                    #         'job_id': job_id,
                    #         'email_from': rec.email_from,
                    #         'partner_name': rec.partner_name,
                    #         # 'message_ids' : rec.messa
                    #     })

                    #     messages = self.env['mail.message'].search([
                    #         ('model', '=', 'hr.applicant'),
                    #         ('res_id', '=', rec.id)
                    #     ])

                    #     # Post messages on new applicant
                    #     for msg in messages:
                    #         new_applicant.message_post(
                    #             body=msg.body,
                    #             subject=msg.subject,
                    #             message_type=msg.message_type or 'comment',
                    #             subtype_id=msg.subtype_id.id if msg.subtype_id else False,
                    #             author_id=msg.author_id.id if msg.author_id else False,
                    #             email_from=msg.email_from,
                    #         )
                    break

    @api.model
    def create(self, vals):
        res = super().create(vals)

        res.trigger_applicant_based_on_job()

        return res

