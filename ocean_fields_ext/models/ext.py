from odoo import models, api
from datetime import datetime
import time
from odoo.exceptions import UserError

class FetchMailServer(models.Model):
    _inherit = 'fetchmail.server'

    def fetch_mail(self):
        # raise UserError("Check")
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

        count = 0

        mails = super(FetchMailServer, self).fetch_mail()

        mail_messages = self.env['mail.message'].search([
            ('create_date', '>=', today_start),
            ('create_date', '<=', today_end)
        ])

        for mail in mail_messages:
            if count < 2:
                self._fetch_mails()
                count += 1
            else:
                break

        return mails
