from odoo import api, models


class ReportSaleOrder(models.AbstractModel):
    _name = "report.sale.report_saleorder"
    _description = "Sale Order Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["sale.order"].browse(docids)
        delivery_orders_list = []
        for doc in docs:
            if doc.procurement_group_id:
                delivery_orders = self.env["stock.picking"].search(
                    [("group_id", "=", doc.procurement_group_id.id)]
                )
                delivery_orders_list.append(delivery_orders)

        return {
            "doc_ids": docs.ids,
            "doc_model": "sale.order",
            "docs": docs,
            "proforma": True,
            "delivery_orders_list": delivery_orders_list,
        }
