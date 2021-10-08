# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection(selection_add=[("append", "Append")])
    discount = fields.Float(string=_("Discount (%)"), related="partner_id.discount")

    def action_append(self):
        self.write({"state": "append"})

    def action_confirm_append(self):
        self.write({"state": "purchase"})

    def _amount_all(self):
        super(PurchaseOrder, self)._amount_all()
        self.write(
            {
                "amount_total": self.amount_total
                - ((self.amount_total * self.discount) / 100)
            }
        )
