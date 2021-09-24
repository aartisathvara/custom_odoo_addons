import calendar
from ast import literal_eval
from datetime import datetime

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def _get_domain(self):
        # first method
        current_year, current_month = datetime.now().year, datetime.now().month
        _, numbers_of_days = calendar.monthrange(current_year, current_month)
        first_day, last_day = datetime.today().replace(day=1), datetime.today().replace(
            day=numbers_of_days
        )
        partners = (
            self.env["sale.order"]
            .search([("date_order", ">=", first_day), ("date_order", "<=", last_day)])
            .mapped("partner_id")
        )

        # second method usinf mapped and filtered method
        # partners = self.env['sale.order'].search([]).filtered(lambda l: l.date_order.month == datetime.today().month).mapped("partner_id")

        return [("id", "in", partners.ids)]

    module_sale_management = fields.Boolean("Sales")
    # group_sale_delivery_address = fields.Boolean("Customer Addresses",
    # 					implied_group='sale.group_delivery_invoice_address')
    teacher_active = fields.Boolean(
        "Teacher Active Boolean", config_parameter="school.teacher_active"
    )
    teacher_active_name = fields.Char(
        "Teacher Active Name", config_parameter="school.teacher_name"
    )
    primary_school = fields.Char("Primary School")
    partner_ids = fields.Many2many(
        "res.partner",
        "partner_schhol_rel",
        "school_id",
        "partner_id",
        string="Partners",
        domain=_get_domain,

    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res["primary_school"] = self.env["ir.config_parameter"].get_param(
            "school.primary_school"
        )
        partner_ids = self.env["ir.config_parameter"].get_param("school.partner_ids")
        res.update(
            partner_ids=[(6, 0, literal_eval(partner_ids))],
        )
        return res

    def set_values(self):
        self.env["ir.config_parameter"].set_param(
            "school.primary_school", self.primary_school
        )
        self.env["ir.config_parameter"].set_param(
            "school.partner_ids", self.partner_ids.ids
        )
        return super(ResConfigSettings, self).set_values()
