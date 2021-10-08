# -*- coding: utf-8 -*-

from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CustomerDocument(models.Model):
    _name = "customer.document"
    _description = "Customer Document"

    name = fields.Char("Name", related="partner_id.name")
    birth_date = fields.Date("Birth Date")
    expiry_date = fields.Date("Expiry Date")
    age = fields.Char("Age", readonly="1")
    partner_id = fields.Many2one("res.partner", "Customer", required="1")
    document_count = fields.Integer(
        string="# Document", compute="compute_document_count"
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("approved", "Approved"),
            ("expired", "Expired"),
            ("refused", "Refused"),
        ],
        "Status",
        default="draft",
    )

    @api.onchange("expiry_date")
    def _compute_state(self):
        if self.expiry_date == date.today():
            self.write({"state": "expired"})

    def action_draft(self):
        for record in self:
            record.write({"state": "draft"})

    def action_approved(self):
        for record in self:
            record.write({"state": "approved"})

    def action_refused(self):
        for record in self:
            record.write({"state": "refused"})

    # count document
    def compute_document_count(self):
        for document in self:
            document.document_count = self.env["customer.document"].search_count([])

    # calculate_age function
    def calculate_age(self):
        for record in self:
            if record.birth_date:
                age = date.today().year - record.birth_date.year
                record.age = str(age) + " years"
                if age < 18:
                    raise UserError(_("The customer age cannot be less than 18 years."))
            else:
                raise UserError(_("Please select birth date than calculate age."))
