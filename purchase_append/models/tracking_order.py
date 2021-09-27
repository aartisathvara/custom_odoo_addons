from odoo import fields, models
from odoo.tools.translate import _

class TrackingOrder(models.Model):
    _name = "tracking.order"
    _description = "Order tracking"

    sales_order_ref = fields.Many2one("sale.order", string=_("Sales Order"))
    user_name = fields.Many2one("res.users", string=_("User Name"))
