from odoo import _, api, fields, models


class CreateSaleOrderWizard(models.TransientModel):
    _name = "create.sale.order.wizard"
    _description = "create_sale_order_wizard"

    order_date = fields.Datetime(
        string="Order Date", default=lambda self: fields.Datetime.now(), required=True
    )
    sale_order_line = fields.One2many(
        "order.line", "order_line_id", string="Order Line", required=True
    )

    def create_sale_order(self):
        global sale_order
        order_line_vals = []
        for line in self.sale_order_line:
            order_line_vals += [
                (
                    0,
                    0,
                    {
                        "product_id": line.product_id.id,
                        "product_uom_qty": line.product_qty,
                        "price_unit": line.product_unit_price,
                    },
                )
            ]
        sale_order_list = []
        for active_id in self._context.get("active_ids"):
            sale_order = self.env["sale.order"].create(
                {
                    "partner_id": active_id,
                    "date_order": self.order_date,
                    "order_line": order_line_vals,
                }
            )
            sale_order_list.append(sale_order)
        if len(sale_order_list) > 1:
            views = [
                (self.env.ref("sale.view_quotation_tree").id, "tree"),
                (self.env.ref("sale.view_order_form").id, "form"),
            ]
            return {
                "name": _("Sale Order)"),
                "view_mode": "form,tree",
                "res_model": "sale.order",
                "view_id": False,
                "report": views,
                "type": "ir.actions.act_window",
            }
        else:
            return {
                "view_type": "form",
                "view_mode": "form",
                "res_model": "sale.order",
                "res_id": sale_order.id or False,
                "type": "ir.actions.act_window",
            }


class SaleOrderLine(models.TransientModel):
    _name = "order.line"
    _description = "order_line"

    name = fields.Text(string="Description")
    order_line_id = fields.Many2one("create.sale.order.wizard", string="Order id")
    product_id = fields.Many2one("product.product", string="Product", required=True)
    product_qty = fields.Float(string="Quantity", default=1.0)
    product_unit_price = fields.Float("Unit Price", default=0.0)

    @api.onchange("product_id")
    def _product_unit_price(self):
        self.product_unit_price = self.product_id.lst_price
        self.name = self.product_id.name
