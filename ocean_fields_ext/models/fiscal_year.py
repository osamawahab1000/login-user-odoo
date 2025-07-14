from odoo import fields, models, api, _
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta


class FiscalYear(models.Model):
    _name = "fiscal.year"

    name= fields.Char(string="Name")
    date_start= fields.Date(string="Date Start")
    date_end= fields.Date(string="Date End")
    month_name = fields.Char(string="Month", compute="_compute_end_month")

    @api.depends('date_end')
    def _compute_end_month(self):
        for record in self:
            if record.date_end:
                next_month_date = record.date_end + relativedelta(months=1)
                record.month_name = next_month_date.strftime('%B %Y')
            else:
                record.month_name = ''



