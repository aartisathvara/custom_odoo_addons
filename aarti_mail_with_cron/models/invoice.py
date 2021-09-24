from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, models

class AccountMove(models.Model):
    _inherit = "account.move"

    def invoice_cron(self):
        next_due_date = date.today() + relativedelta(months=1)
        invoices = self.env["account.move"].search(
            [
                ("move_type", "=", "out_invoice"),
                ("state", "=", "posted"),
                ("payment_state", "in", ["not_paid", "partial"]),
                ("invoice_date_due", "=", next_due_date),
            ]
        )
        for invoice in invoices:
            template = self.env.ref("aarti_mail_with_cron.invoice_email_template")
            template.send_mail(invoice.id,force_send=True)

#email_value
# raise_if_not_found=False