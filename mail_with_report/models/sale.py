from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_quotation_send_aarti(self):
        template = self.env.ref("mail_with_report.email_template_sale")
        ctx = {
            "default_model": "sale.order",
            "default_res_id": self.ids[0],
            "default_template_id": template.id,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }
